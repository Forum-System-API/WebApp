import datetime

from data.database import read_query, update_query, insert_query
from data.models import Message
from routers.user import User
from datetime import datetime, timedelta
from services.secret import secret_key


def all(logged_user: User):
    data = read_query('''SELECT message_id, text, timestamp, sender_id, recipient_id FROM message
    WHERE recipient_id = ? OR sender_id = ?''', (logged_user.id, logged_user.id))
    return data


def write_message(message_text, recipient_id: int, sender_id: int, message_timestamp) -> Message | None:
    insert_query('''INSERT INTO messages(text, timestamp, sender_id, recipient_id)
    VALUES(?, ?, ?, ?, ?)''', (message_text, message_timestamp, sender_id, recipient_id))
    pass
