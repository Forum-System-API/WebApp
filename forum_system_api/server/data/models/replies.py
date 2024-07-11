from datetime import datetime
from pydantic import BaseModel, constr


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