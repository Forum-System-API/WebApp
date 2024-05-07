import datetime

from data.database import read_query, update_query, insert_query
from data.models import Message
from routers.user import User
from datetime import datetime, timedelta
from services.secret import secret_key


def all(logged_user: User):
    data = read_query('''SELECT message_id, text, timestamp, sender_id, recipient_id FROM messages
    WHERE recipient_id = ? OR sender_id = ?''', (logged_user.id, logged_user.id))
    return data


def write_message(message: Message) -> Message | None:
    generated_id = insert_query('''INSERT INTO messages(message_id, text, timestamp, sender_id, recipient_id)
    VALUES(?, ?, ?, ?, ?)''', (message.message_id, message.text, message.timestamp, message.sender_id, message.recipient_id))

    message.message_id = generated_id

    return message
