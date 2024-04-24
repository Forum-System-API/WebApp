from pydantic import BaseModel, constr


TUsername = constr(pattern='^\w{2,30}$')


class Role:
    ADMIN = "admin"
    ORDINARY_USER = "basic_user"

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
    pass 

class Message(BaseModel): # - Valkata
    pass 

class Topic(BaseModel): # - Elena
    pass 

class Reply(BaseModel): # - Elena
    pass 
