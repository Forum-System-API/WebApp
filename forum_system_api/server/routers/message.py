from fastapi import APIRouter, Response, Header
from data.models import Message
from services.user_service import find_by_username
from services import message_service, user_service
from common.auth import get_user_or_raise_401
from datetime import datetime

message_router = APIRouter(prefix='/messages')


@message_router.get('/')
def view_conversations(x_token=Header()):
    logged_user = get_user_or_raise_401(x_token)
    messages = message_service.view_all(logged_user)
    return messages


@message_router.get('/{username}')
def view_conversations(username, x_token=Header()):
    logged_user = get_user_or_raise_401(x_token)
    recipient = find_by_username(username)
    messages = message_service.view_conversation(recipient, logged_user)
    return messages


@message_router.post('/send/{username}')
def send_message(message: Message, username, x_token=Header()):
    logged_user = get_user_or_raise_401(x_token)
    recipient = find_by_username(username)
    message.recipient_id = recipient.id
    message.sender_id = logged_user.id
    message.timestamp = datetime.now()
    message_service.write_message(message)
    return "Message successfully sent!"


#Messages should be deleted only for the logged user instead of all messages with the logged user's id
@message_router.delete('/all')
def delete_message_history(x_token=Header()):
    logged_user = get_user_or_raise_401(x_token)
    message_service.delete_all(logged_user.id)
    return "Message history deleted"
