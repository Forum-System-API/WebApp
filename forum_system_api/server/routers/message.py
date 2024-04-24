from fastapi import APIRouter, Response
from data.models import Message
from services import message_service


message_router = APIRouter(prefix='/message')


@message_router.get("/read")
def show_all_messages():
    pass

@message_router.post("/")
def send_message():
    pass