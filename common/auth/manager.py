from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from loguru import logger

import config
from common import db


class UserManager(IntegerIDMixin, BaseUserManager[db.User, int]):
    reset_password_token_secret = config.JWT_VERIFY_SECRET
    verification_token_secret = config.JWT_VERIFY_SECRET

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Request | None = None,
    ) -> models.UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        Params:
            user_create: The UserCreate model to create.
            safe: If True, sensitive values like is_superuser or is_verified
            will be ignored during the creation, defaults to False.
            request: Optional FastAPI request that
            triggered the operation, defaults to None.

        Raises:
            UserAlreadyExists: A user already exists with the same e-mail.

        Returns:
            A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        if safe:
            user_dict = user_create.create_update_dict()
        else:
            user_dict = user_create.create_update_dict_superuser()

        password = user_dict.pop('password')
        user_dict['hashed_password'] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)
        await self.on_after_register(created_user, request)
        return created_user

    async def on_after_register(
        self,
        user: db.User,
        request: Request | None = None,
    ):
        logger.info('User id="%s" has registered', user.id)


async def get_user_db(session: db.AsyncSession = Depends(db.get_session)):
    yield SQLAlchemyUserDatabase(session, db.User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
