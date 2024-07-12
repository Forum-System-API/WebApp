from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from data.models.replies import Reply

class Topic(BaseModel):  
    topic_id: Optional[int] = None
    title: str
    date_time: Optional[datetime] = None
    category_id: int
    user_id: Optional[int] = None
    best_reply: Optional[str] = None
    is_locked: Optional[int] = 0 #if is_locked = 0, the topic is inlocked; if is_locked = 1, the topic is locked;

    @classmethod
    def from_query_result(cls, topic_id, title, date_time, category_id, user_id, best_reply, is_locked):
        
        # if best_reply is None:
        #     best_reply = 'No best reply has been chosen yet.'

        return cls(topic_id=topic_id,
                   title=title,
                   date_time=date_time,
                   category_id=category_id,
                   user_id=user_id,
                   best_reply=best_reply,
                   is_locked=is_locked)

class TopicView(BaseModel):
    topic: Topic
    replies: list[Reply]

class TopicViewAll(BaseModel):
    title: str
    date_time: str
    status: str

    @classmethod
    def topic_view_all(cls, topic, title, date_time, status):
        return cls(title=topic.title,
                   date_time=topic.date_time.strftime('%Y/%m/%d %H:%M'),
                   status=status)

class TopicUpdate(BaseModel):
    best_reply: str | None =  None
    reply_id: int | None = None

