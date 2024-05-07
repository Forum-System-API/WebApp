from fastapi import APIRouter, Response, Header
from data.models import Message
from services import message_service, user_service
from common.auth import get_user_or_raise_401
from datetime import datetime


message_router = APIRouter(prefix='/messages')


@message_router.get('/')
def show_all_messages(x_token):    # Accepts token which find who the logged user is in order to show the logged user's messages
    logged_user = get_user_or_raise_401(x_token)
    messages = message_service.all(logged_user)
    return messages

@message_router.post('/send/{username}')   # Change to noun how?
def send_message(message: Message, x_token = Header()):
    logged_user = get_user_or_raise_401(x_token)
    message.sender_id = logged_user.id
    message_timestamp = datetime.now()
    message_service.write_message(message_text=message.text, recipient_id=message.recipient_id,
                                  sender_id=message.message_author, message_timestamp=message_timestamp)