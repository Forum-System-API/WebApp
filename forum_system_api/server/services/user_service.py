from data.database import read_query,update_query,insert_query
from data.models import User,Role
from mariadb import IntegrityError
import jwt
from datetime import datetime, timedelta
from services.config import secret_key


def all():
    data = read_query('''SELECT username, password, role FROM users''')
    return data

def create(username:str, password:str) -> User|None:
    
    existing_user = read_query(
        'SELECT username FROM users WHERE username = ?', (username,)
    )
    
    if existing_user:
        return None
    
    try:
        generated_id = insert_query(
            'INSERT INTO users(username, password, role) VALUES(?,?,?)',
            (username, password, Role.ORDINARY_USER )
        )
        return User(id = generated_id, username = username, password ='', role = Role.ORDINARY_USER)
    
    except IntegrityError:
        return None
    
    
def find_by_username(username: str) -> User | None:
    data = read_query(
        'SELECT user_id, username, password, role FROM users WHERE username = ?',
        (username,))

    return next((User.from_query_result(*row) for row in data), None)

def try_login(username: str, password: str) -> User | None:
    user = find_by_username(username)

    return user if user and user.password == password else None

def create_token(user: User) -> str:
    
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.now() + timedelta(hours=1)
    }

   
    token = jwt.encode(payload, secret_key, algorithm='HS256')

    return token


def promote_user_to_admin(username:str):
    user = User.get(username=username)
    
    if user:
        update_query('''UPDATE users SET role = ? WHERE username = ?''',(Role.ADMIN, username))
        user.role = Role.ADMIN
        return user
    else:
        return None