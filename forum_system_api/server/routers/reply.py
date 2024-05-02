from fastapi import APIRouter, Response
from data.models import Reply
from services import reply_service


reply_router = APIRouter(prefix='/replies')

# creates a new reply to a certain topic
@reply_router.post('/', status_code=201)
def create_reply(reply: Reply):
     if not reply_service.topic_exists(reply.topic_id):
        return Response(status_code=400,
                        content=f'Topic {reply.topic_id} does not exist')

     return reply_service.create(reply)


# updates a repply
@reply_router.put('/{id}')
def update_reply(id: int, reply: Reply):
     if not reply_service.category_exists(reply.topic_id):
        return Response(status_code=400,
                        content=f'Topic {reply.topic_id} does not exist')

     existing_reply = reply_service.get_by_id(id)
     if existing_reply is None:
        return Response(status_code=404)
     else:
        return reply_service.update(existing_reply, reply)


# deletes a repply
@reply_router.delete('/{id}')
def delete_reply(id: int):
    reply_service.delete(id)

    return Response(status_code=204)
