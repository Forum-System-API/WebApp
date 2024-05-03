from data.database import read_query,update_query,insert_query
from data.models import Message
#from datetime import datetime, timedelta
from services.config import secret_key


def all(message_recipient):
    data = read_query('''SELECT message_id, message_text, message_timestamp, message_author, message_recipient FROM message
    WHERE message_recipient = ?''', (message_recipient,))
    return data

def write_message(recipient: str) -> Message | None:
    pass