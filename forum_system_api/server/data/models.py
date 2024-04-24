import datetime

from pydantic import BaseModel, constr
from enum import Enum

TUsername = constr(pattern='^\w{2,30}$')


class RoleEnum(str, Enum):
    admin = "admin"
    basic_user = "basic_user"

class Role(BaseModel):
    role: RoleEnum

    class Config:
        use_enum_values = True

class User(BaseModel):
    id: int | None = None
    username: str
    password:str
    role: Role
    # is_admin = False
   
    

    def promote_to_admin(self):
        self.role = Role.ADMIN
        # self.is_admin = True
    
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

class Category(BaseModel): # - Valkata
    category_id: int | None = None
    category_name: str

    @classmethod
    def from_query_result(cls, category_id, category_name):
        return cls(
            category_id=category_id,
            category_name=category_name
        )

class Message(BaseModel): # - Valkata
    message_id: int | None = None
    message_text: str
    message_timestamp: datetime.date
    message_author: User
    message_recipient: User

class Topic(BaseModel): # - Elena
    pass 

class Reply(BaseModel): # - Elena
    pass 
