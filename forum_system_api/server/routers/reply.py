from fastapi import APIRouter, Response
from data.models import Reply
from services import reply_service, topic_service

replies_router = APIRouter(prefix='/replies')

# available for: admin, user - requires authentication token
@replies_router.post('/', status_code=201)
def create_reply(reply: Reply):
   if not topic_service.exists(reply.topic_id):
      return Response(status_code=400, content=f'Topic {reply.topic_id} does not exist.')

   return reply_service.create(reply)

# available for: user - requires authentication token
@replies_router.put('/{reply_id}')
def update_reply(reply_id: int, reply: Reply):
   if not topic_service.exists(reply.topic_id):
      return Response(status_code=400, content=f'Topic {reply.topic_id} does not exist.')

   existing_reply = reply_service.get_by_id(reply_id)
   if existing_reply is None:
      return Response(status_code=404)
   else:
      return reply_service.update(existing_reply, reply)

# available for: user - requires authentication token
@replies_router.delete('/{reply_id}')
def delete_reply(reply_id: int):
   reply_service.delete(reply_id)

   return Response(status_code=204)
