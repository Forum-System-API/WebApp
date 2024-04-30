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


# # Elena - changes to follow
# class Topic(BaseModel): 
#     id: int 
#     title: str
#     category_id: int
#     author_id: int # not sure? 
#     user_ids: list[int]  # not needed - do this instead - v replies da se syhranqvat id-tata na users // ne moje da ima 3 best replie , ima samo edin zatova tuk

#     @classmethod
#     def from_query_result(cls, id, title, category_id, user_ids=[]):
#         return cls(
#             id=id,
#             title=title,
#             category_id=category_id,
#             user_ids=user_ids)

# class UpdateTopic:
#     title: str
#     category_id: int

# # time,date? - kato v messages - sortiraneto da e s ID-to
# class Reply(BaseModel): 
#     id: int | None
#     text: str
#     upvotes: int 
#     downvotes: int
#     topic_id: int
#     topic_category_id: int # not needed
#     user_id: int
#     # is_best: False ? not sure how to make a reply the best one? - not needed for every reply 

#     @classmethod
#     def from_query_result(cls, id, text, upvotes, downvotes, topic_id, topic_category_id, user_id, is_best):
#         return cls(
#             id=id,
#             text=text,
#             upvotes=upvotes,
#             downvotes=downvotes,
#             topic_id=topic_id,
#             topic_category_id=topic_category_id,
#             user_id=user_id,
#             is_best=is_best)

# class UpdateReply:
#     text: str
#     upvotes: int 
#     downvotes: int