from datetime import datetime
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
        
class Category(BaseModel): # - Valkata
    category_id: int | None = None
    category_name: str
    is_private:int | None = None
    is_locked:int | None = None

    @classmethod
    def from_query_result(cls, category_id, category_name, is_private, is_locked):
        return cls(
            category_id=category_id,
            category_name=category_name,
            is_private = is_private,
            is_locked = is_locked
        )

class Message(BaseModel): # - Valkata
    message_id: int | None = None
    text: str | None = None
    timestamp: datetime | None = None
    sender_id: int | None = None
    recipient_id: int | None = None

class Topic(BaseModel):  
    topic_id: int | None = None
    title: str
    date_time: datetime | None = None
    category_id: int
    user_id: int | None = None
    best_reply: str | None = None
    is_locked: int | None = None

    @classmethod
    def from_query_result(cls, topic_id, title, date_time, category_id, user_id, best_reply, is_locked):
        if best_reply is None:
            best_reply = 'No best reply yet.'

        if is_locked is None:
            is_locked = 'Unlocked.'
       
        return cls(
            topic_id=topic_id,
            title=title,
            date_time=date_time,
            category_id=category_id,
            user_id=user_id,
            best_reply=best_reply,
            is_locked=is_locked,
            )

class TopicUpdate(BaseModel):
    best_reply: str | None =  None

class Reply(BaseModel): 
    reply_id: int | None = None
    text: str
    date_time: datetime | None = None
    topic_id: int
    user_id: int | None = None

    @classmethod
    def from_query_result(cls, reply_id, text, date_time, topic_id, user_id):
        return cls(
            reply_id=reply_id,
            text=text,
            date_time=date_time,
            topic_id=topic_id,
            user_id=user_id,
            )
    
class ReplyUpdate(BaseModel):
    text: str | None =  None

class Vote(BaseModel):
    reply_id: int 
    user_id: int | None = None
    type_of_vote: int | None = None

    @classmethod
    def from_query_result(cls, reply_id, user_id, type_of_vote):
        if type_of_vote is None:
            type_of_vote = 'No votes yet.'
       
        return cls(
            reply_id=reply_id,
            user_id=user_id,
            type_of_vote=type_of_vote
            )
    
class Categories_Access(BaseModel):
    user_id: int
    category_id: int
    can_read: int = 1
    can_write: int = 1
