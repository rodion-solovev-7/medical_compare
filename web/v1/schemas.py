from fastapi_users import schemas, models
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    name: str


class UserCreate(schemas.BaseUserCreate):
    id: models.ID
    email: EmailStr
    name: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserUpdate(schemas.BaseUserUpdate):
    name: str
