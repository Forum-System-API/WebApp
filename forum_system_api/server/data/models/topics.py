from datetime import datetime
from pydantic import BaseModel, constr
from data.models.replies import Reply


class Topic(BaseModel):  
    topic_id: int | None = None
    title: str
    date_time: datetime | None = None
    category_id: int
    user_id: int | None = None
    best_reply: str | None = None
    is_locked: constr(pattern='^locked|unlocked$') = "unlocked"

    @classmethod
    def from_query_result(cls, topic_id, title, date_time, category_id, user_id, best_reply, is_locked):
        if best_reply is None:
            best_reply = 'no best reply yet'

        return cls(
            topic_id=topic_id,
            title=title,
            date_time=date_time,
            category_id=category_id,
            user_id=user_id,
            best_reply=best_reply,
            is_locked='locked' if is_locked else 'unlocked',
            )


class TopicResponseModel(BaseModel):
    topic: Topic
    replies: list[Reply]


class TopicUpdate(BaseModel):
    best_reply: str | None =  None
    reply_id: int | None = None

