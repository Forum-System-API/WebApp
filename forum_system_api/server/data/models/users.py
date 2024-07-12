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