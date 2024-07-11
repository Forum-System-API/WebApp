from datetime import datetime
from pydantic import BaseModel, constr


TUsername = constr(pattern='^\\w{2,30}$')



class Role:
    ADMIN = 'admin'
    ORDINARY_USER = 'basic_user'

class User(BaseModel):
    id: int | None = None
    username: str
    password:str
    role: str = Role.ORDINARY_USER
   
    @classmethod
    def from_query_result(cls, user_id, username, password, role ):
        return cls(
            id=user_id,
            username=username,
            password=password,
            role=role
        )
        
class LoginData(BaseModel):
    username: TUsername
    password: str
        
class Category(BaseModel): 
    category_id: int | None = None
    category_name: str
    is_private: int = 0
    is_locked: int = 0

    @classmethod
    def from_query_result(cls, category_id, category_name, is_private, is_locked):
        return cls(
            category_id=category_id,
            category_name=category_name,
            is_private = is_private,
            is_locked = is_locked
        )


class Categories_Access(BaseModel):
    user_id: int
    category_id: int
    can_read: int = 1
    can_write: int = 1
