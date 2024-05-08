from data.database import read_query, update_query, insert_query
from data.models import User, Role
from mariadb import IntegrityError
import jwt
from datetime import datetime, timedelta
from services.secret import secret_key
from hashlib import sha256

_SEPARATOR = ';'


def all():
    data = read_query('''SELECT username, password, role FROM users''')
    return data


def create(username: str, password: str) -> User | None:
    existing_user = read_query(
        'SELECT username FROM users WHERE username = ?', (username,)
    )

    if existing_user:
        return None

    hashed_password = _hash_password(password)

    try:
        generated_id = insert_query(
            'INSERT INTO users(username, password, role) VALUES(?,?,?)',
            (username, hashed_password, Role.ORDINARY_USER)
        )
        return User(id=generated_id, username=username, password='', role=Role.ORDINARY_USER)

    except IntegrityError:
        return None


def find_by_username(username: str) -> User | None:
    data = read_query(
        'SELECT user_id, username, password, role FROM users WHERE username = ?',
        (username,))

    return next((User.from_query_result(*row) for row in data), None)


def try_login(username: str, password: str) -> User | None:
    user = find_by_username(username)

    if user and verify_password(password, user.password):
        return user
    else:
        return None


def create_token(user: User) -> str:
    return f'{user.id}{_SEPARATOR}{user.username}'


def is_authenticated(token: str) -> bool:
    user_id, username = token.split(_SEPARATOR)
    user = read_query(
        '''SELECT user_id, username, password, role FROM users WHERE user_id = ? AND username = ?''',
        (int(user_id), username)
    )
    if user:
        data = user[0]

        authenticated = bool(data[0] == int(user_id) and data[1] == username)

        return authenticated
    else:
        return False


def from_token(token: str) -> User | None:
    _, username = token.split(_SEPARATOR)
    return find_by_username(username)


def _hash_password(password: str) -> str:
    return sha256(password.encode('utf-8')).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    return hashed_password == _hash_password(password)


def change_role(username:str, role:str):
    if role not in (Role.ADMIN, Role.ORDINARY_USER, Role.GUEST):
        raise ValueError('Invalid role')
    
    user = update_query('''UPDATE users SET role = ? where username = ?''',(role, username))
    return user