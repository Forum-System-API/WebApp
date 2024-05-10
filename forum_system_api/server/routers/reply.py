from fastapi import APIRouter, Header
from common.responses import NotFound, BadRequest, InternalServerError, Unauthorized, NoContent
from common.auth import get_user_or_raise_401
from data.models import Reply, ReplyUpdate
from services import reply_service, topic_service, user_service
from datetime import datetime

replies_router = APIRouter(prefix='/replies')


@replies_router.post('/')  # available for: admin, user - token
def create_reply(reply: Reply, x_token: str = Header()):
   user = get_user_or_raise_401(x_token)

   reply.date_time = datetime.now()
   reply.date_time = reply.date_time.strftime("%Y/%m/%d %H:%M")
   
   if not topic_service.topic_id_exists(reply.topic_id):
      return BadRequest(content=f'Topic {reply.topic_id} does not exist.') # status_code=400

   return reply_service.create(reply, user)


@replies_router.put('/{reply_id}')  # available for: admin, user - token
def update_reply(reply_id: int, data: ReplyUpdate, x_token: str = Header()):
   user = get_user_or_raise_401(x_token)

   # reply.date_time = datetime.now()
   # reply.date_time = reply.date_time.strftime("%Y/%m/%d %H:%M")

   reply = reply_service.get_by_id(reply_id)
   if reply is None:
      return NotFound()  # status_code=404

   if not user_service.owns_reply(user, reply):
      return Unauthorized('Can`t edit others` replies.')  # status_code=401

   reply = reply_service.update(data, reply)

   if reply:
      return reply
   else:
      InternalServerError()  # status_code=500


@replies_router.delete('/{reply_id}')  # available for: admin, user - token
def delete_reply(reply_id: int, x_token: str = Header()):
   user = get_user_or_raise_401(x_token)

   reply = reply_service.get_by_id(reply_id)
   if reply is None:
      return NotFound()  # status_code=404

   if not user_service.owns_reply(user, reply):
      return Unauthorized('Can`t edit others` replies.')  # status_code=401

   reply_service.delete(reply)

   return NoContent()  # status_code=204
