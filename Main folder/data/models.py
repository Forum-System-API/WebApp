from pydantic import BaseModel, constr


TUsername = constr(pattern='^\w{2,30}$')


class Role:
    ADMIN = "admin"
    ORDINARY_USER = "basic_user"

class User(BaseModel):
    id: int | None = None
    username: str
    password:str
    role: str
   
    

    def is_admin(self):
        return self.role == 'Admin'
    
    @classmethod
    def from_query_result(cls, id, username, password, role):
        return cls(
            id=id,
            username=username,
            password=password,
            role=role
        )
        
class LoginData(BaseModel):
    username: TUsername
    password: str