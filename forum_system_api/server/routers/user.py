from fastapi import APIRouter, Response, status, HTTPException
from data.models import User, LoginData
from services import user_service


users_router = APIRouter(prefix='/users')


@users_router.get('/')
def get_users(sort: str | None=None):
    
    users = user_service.all()
    
    if sort and (sort == 'asc' or sort == 'desc'):
        return user_service.sort(users, reverse=sort=='desc')
    else:
        return users

@users_router.post('/register')
def register(data: LoginData, response: Response):
    user = user_service.create(data.username, data.password)
    
   
    if user:
        return "Registration completed!"
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return{"message":f"Username {data.username} is taken." }
    
    
@users_router.post('/login')
def login(data: LoginData):
    user = user_service.try_login(data.username, data.password)

    if user:
        token = user_service.create_token(user)
        return {'token': token}
    else:
        raise HTTPException(status_code=401, detail='Invalid username or password')
    
    
@users_router.post('/promote/{username}')
def promote_user_to_admin(username: str):
    user = user_service.promote_user_to_admin(username)
    
    if user:
        return {"message": f"User {user.username} promoted to admin successfully."}
    else:
        raise HTTPException(status_code=404, detail="User not found")