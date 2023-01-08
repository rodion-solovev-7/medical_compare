from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers

from common import db
from common.auth.auth import auth_backend
from common.auth.manager import get_user_manager
from web.v1.schemas import UserRead, UserCreate, UserUpdate

app = FastAPI()

fastapi_users = FastAPIUsers[db.User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/jwt',
    tags=['auth'],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='',
    tags=['auth'],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='',
    tags=['auth'],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix='',
    tags=['auth'],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='',
    tags=['users'],
)

@app.get('/get-user-email')
def get_current_user_email(user: db.User = Depends(current_user)):
    return user.email


@app.get('/')
def get_current_user_data(user: db.User = Depends(current_user)):
    return {
        'name': user.name,
        'email': user.email
    }
