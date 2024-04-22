from data.database import read_query,update_query,insert_query
from data.models import User,Role
from mariadb import IntegrityError


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