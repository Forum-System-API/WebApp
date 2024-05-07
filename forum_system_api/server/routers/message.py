from fastapi import APIRouter, Response, Header
from data.models import Message
from services.user_service import find_by_username
from services import message_service, user_service
from common.auth import get_user_or_raise_401
from datetime import datetime

message_router = APIRouter(prefix='/messages')


@message_router.get('/')
def show_all_messages(
        x_token=Header()):  # Accepts token which find who the logged user is in order to show the logged user's messages
    logged_user = get_user_or_raise_401(x_token)
    messages = message_service.all(logged_user)
    return messages


@message_router.post('/send/{username}')
def send_message(message: Message, username, x_token=Header()):
    logged_user = get_user_or_raise_401(x_token)
    recipient = find_by_username(username)
    message.recipient_id = recipient.id
    message.sender_id = logged_user.id
    message.timestamp = datetime.now()
    message_service.write_message(text=message.text, recipient_id=message.recipient_id,
                                  sender_id=message.sender_id, timestamp=message.timestamp)
