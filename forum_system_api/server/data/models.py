from datetime import datetime, date
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
    text: str | None = None
    timestamp: datetime | None = None
    sender_id: int | None = None
    recipient_id: int | None = None

class Topic(BaseModel): 
    topic_id: int 
    title: str
    category_id: int
    user_id: int
    date_time: datetime
    # best_reply_id: int 
    # status_locked: constr(pattern='^unlocked|locked$')
    # status_private: constr(pattern='^public|private$')
 
    @classmethod
    def from_query_result(cls, topic_id, title, category_id, user_id, date_time): # add: 1. is_locked 2. is_private  3. replies = None - not sutre yet
        return cls(
            topic_id=topic_id,
            title=title,
            category_id=category_id,
            user_id=user_id,
            date_time=date_time)
        # status_locked='unlocked' if not is_locked else 'locked' - not sure yet
        # status_private='public' if not is_private else 'private' - not sure yet
        
class Reply(BaseModel): 
    reply_id: int 
    text: str
    topic_id: int
    user_id: int
    date_time: datetime

    @classmethod
    def from_query_result(cls, reply_id, text, topic_id, user_id, date_time):
        return cls(
            reply_id=reply_id,
            text=text,
            topic_id=topic_id,
            user_id=user_id,
            date_time=date_time)