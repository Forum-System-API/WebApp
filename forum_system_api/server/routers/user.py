from fastapi import APIRouter, Response, status, HTTPException, Header
from data.models import User, LoginData, Role
from services import user_service
import jwt
from services.secret import secret_key
from common.auth import get_user_or_raise_401

users_router = APIRouter(prefix='/users')


@users_router.get('/')
def get_users(sort: str | None = None):
    users = user_service.all()

    if sort and (sort == 'asc' or sort == 'desc'):
        return user_service.sort(users, reverse=sort == 'desc')
    else:
        return users


@users_router.post('/register')
def register(data: LoginData, response: Response):
    user = user_service.create(data.username, data.password)

    if user:
        return 'Registration completed!'
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': f'Username {data.username} is taken.'}


@users_router.post('/login')
def login(data: LoginData):
    user = user_service.try_login(data.username, data.password)

    if user:
        if user.username == 'admin':
            user.role = Role.ADMIN
            token = user_service.create_token(user)
            return {'token': token}
        else:
            user.role = Role.ORDINARY_USER
            token = user_service.create_token(user)
            return {'token': token}

    else:
        raise HTTPException(status_code=401, detail='Invalid username or password')


@users_router.get('/info')
def user_info(x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    return {'username': user.username, 'role': user.role}

@users_router.post('/new_role')
def change_role(data: User, x_token: str = Header()):
    
    if x_token.split(';')[1] != Role.ADMIN:
        raise HTTPException(status_code=403, detail = 'Admin credentials required')
    
    user = user_service.find_by_username(data.username)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if data.role not in (Role.ADMIN, Role.ORDINARY_USER, Role.GUEST):
        raise HTTPException(status_code=400, detail="Invalid role")

    
    user_service.change_role(data.username, data.role)

    return f'User role update to {data.role}'