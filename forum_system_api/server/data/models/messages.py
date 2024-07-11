from datetime import datetime
from pydantic import BaseModel, constr



class Message(BaseModel): 
    message_id: int | None = None
    text: str | None = None
    timestamp: datetime | None = None
    sender_id: int | None = None
    recipient_id: int | None = None
