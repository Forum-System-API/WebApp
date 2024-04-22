from fastapi import APIRouter, Response, status
from data.models import User, LoginData
from services import users_services


users_router = APIRouter(prefix='/users')



@users_router.post('/register')
def register(data: LoginData, response: Response):
    user = users_services.create(data.username, data.password)
    
   
    if user:
        return "Registration completed!"
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return{"message":f"Username {data.username} is taken." }
    
    
@users_router.get('/')
def get_users(sort: str | None=None):
    
    users = users_services.all()
    
    if sort and (sort == 'asc' or sort == 'desc'):
        return users_services.sort(users, reverse=sort=='desc')
    else:
        return users
    