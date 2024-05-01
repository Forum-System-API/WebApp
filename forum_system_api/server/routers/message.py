from fastapi import APIRouter, Response
from data.models import Message
from services import message_service


message_router = APIRouter(prefix='/messages')


@message_router.get("/read")    # Change to noun how?
def show_all_messages():    # Accepts token which find who the logged user is in order to show the logged user's messages
    messages = message_service.all(message_recipient=None)

@message_router.post("/send")
def send_message():
    pass