from datetime import datetime
from pydantic import BaseModel, constr

TUsername = constr(pattern='^\w{2,30}$')


class Role:
    ADMIN = 'admin'
    ORDINARY_USER = 'basic_user'
    CUSTOM_USER = "custom_user"
    SUPREME_USER = "supreme_user"


class User(BaseModel):
    id: int | None = None
    username: str
    password: str
    role: str = Role.ORDINARY_USER

    @classmethod
    def from_query_result(cls, user_id, username, password, role):
        return cls(
            id=user_id,
            username=username,
            password=password,
            role=role
        )


class LoginData(BaseModel):
    username: TUsername
    password: str


class Category(BaseModel):  # - Valkata
    category_id: int | None = None
    category_name: str
    is_private: int | None = None
    is_locked: int | None = None

    @classmethod
    def from_query_result(cls, category_id, category_name, is_private, is_locked):
        return cls(
            category_id=category_id,
            category_name=category_name,
            is_private=is_private,
            is_locked=is_locked
        )


class Message(BaseModel):  # - Valkata
    message_id: int | None = None
    text: str | None = None
    timestamp: datetime | None = None
    sender_id: int | None = None
    recipient_id: int | None = None


class Topic(BaseModel):
    topic_id: int | None = None
    title: str
    category_id: int
    user_id: int
    date_time: datetime | None = None

    # best_reply_id: int
    # status_locked: constr(pattern='^unlocked|locked$')
    # status_private: constr(pattern='^public|private$')

    # def __str__(self):
    #     return (
    #     f'topic_id={self.topic_id}\n'
    #     f'title={self.title}\n'
    #     f'category_id={self.category_id}\n'
    #     f'user_id={self.user_id}\n'
    #     f'date_time={self.date_time.strftime("%Y/%m/%d %H:%M")}'
    #     )

    @classmethod
    def from_query_result(cls, topic_id, title, category_id, user_id, date_time):
        # add: 1. is_locked 2. is_private  3. replies = None - not sutre yet
        return cls(
            topic_id=topic_id,
            title=title,
            category_id=category_id,
            user_id=user_id,
            date_time=date_time)
        # status_locked='unlocked' if not is_locked else 'locked' - not sure yet
        # status_private='public' if not is_private else 'private' - not sure yet


class Reply(BaseModel):
    reply_id: int | None = None
    text: str
    topic_id: int
    user_id: int
    date_time: datetime | None = None

    @classmethod
    def from_query_result(cls, reply_id, text, topic_id, user_id, date_time):
        return cls(
            reply_id=reply_id,
            text=text,
            topic_id=topic_id,
            user_id=user_id,
            date_time=date_time)
