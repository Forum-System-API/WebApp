import datetime

from pydantic import BaseModel, constr

TUsername = constr(pattern='^\w{2,30}$')


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


# class Topic(BaseModel): 
#     id: int 
#     title: str
#     category_id: int
#     user_id: int
#     timestamp: datetime
#     best_reply_id: int | None
# #     is_locked: to follow

#     @classmethod
#     def from_query_result(cls, id, title, category_id, user_id, timestamp, best_reply_id):
#         return cls(
#             id=id,
#             title=title,
#             category_id=category_id,
#             user_id=user_id,
#             timestamp=timestamp,
#             best_reply_id=best_reply_id)

# class Reply(BaseModel): 
#     id: int 
#     text: str
#     upvotes: int
#     downvotes: int
#     topic_id: int
#     user_id: int
#     timestamp: datetime

#     @classmethod
#     def from_query_result(cls, id, text, upvotes, downvotes, topic_id, user_id, timestamp):
#         return cls(
#             id=id,
#             text=text,
#             upvotes=upvotes,
#             downvotes=downvotes,
#             topic_id=topic_id,
#             user_id=user_id,
#             timestamp=timestamp)