from fastapi import APIRouter, Query, Header
from common.responses import NotFound, BadRequest, InternalServerError, Unauthorized, NoContent
from common.auth import get_user_or_raise_401
from data.models import Topic, Reply, TopicUpdate
from services import topic_service, reply_service, category_service, user_service
from pydantic import BaseModel
from datetime import datetime

class TopicResponseModel(BaseModel):
    topic: Topic
    replies: list[Reply]


topics_router = APIRouter(prefix='/topics')


@topics_router.get('/') 
def get_topics(sort: str | None = None,
            sort_by: str | None = None, 
            search: str | None = None, 
            page: int = Query(1, gt=0),
            topics_per_page: int = Query(100, gt=0)):
    
    topic_lst = topic_service.all(search)

    start = (page - 1) * topics_per_page
    end = start + topics_per_page
    topic_lst = topic_lst[start:end]

    if sort and (sort == 'asc' or sort == 'desc'):
        return topic_service.sort(topic_lst, reverse=sort == 'desc', attribute=sort_by)
    else:
        return topic_lst


@topics_router.get('/{topic_id}')  
def get_topic_by_id(topic_id: int):
    topic = topic_service.get_by_id(topic_id)

    if topic is None:
        return NotFound() # status_code=404
    else:
        replies=reply_service.get_by_topic(topic.topic_id)
        if replies:
            return TopicResponseModel(topic=topic, replies=reply_service.get_by_topic(topic.topic_id))
        else:
            return (f'{topic}\n'
                    f'There are no replies under this topic.')
    

@topics_router.post('/')  
def create_topic(topic: Topic, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    topic.date_time = datetime.now()
    topic.date_time = topic.date_time.strftime("%Y/%m/%d %H:%M")
    
    if not category_service.category_id_exists(topic.category_id):
        return BadRequest(content=f'Category {topic.category_id} does not exist.') # status_code=400

    return topic_service.create(topic, user)


@topics_router.put('/{topic_id}')  
def update_topic_best_reply(topic_id: int, data: TopicUpdate, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    
    topic = topic_service.get_by_id(topic_id)
    if topic is None:
        return NotFound()  # status_code=404

    if not user_service.owns_topic(user, topic):
        return Unauthorized('Can`t edit others` topics.')  # status_code=401

    topic = topic_service.update(data, topic)

    if topic:
        return topic
    else:
        InternalServerError()  # status_code=500


@topics_router.delete('/{topic_id}')  
def delete_topic(topic_id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    topic = topic_service.get_by_id(topic_id)

    if topic is None:
        return NotFound() # status_code=404

    if not user_service.owns_topic(user, topic):
        return Unauthorized('Can`t delete others` topics.') # status_code=401
    
    topic_service.delete(topic)

    return NoContent() # status_code=204


@topics_router.put('/lock/{topic_id}')
def show_topic_by_id(topic_id: int, x_token=Header()):
    user = get_user_or_raise_401(x_token)

    if user.role != 'admin':
        return BadRequest(content=f'You need administrative rights to lock topics!') # status_code=400
    
    if not topic_service.topic_id_exists(topic_id):
        return BadRequest(content=f'Topic {topic_id} does not exist.')

    topic = topic_service.lock_topic(topic_id)
    return f'Topic {topic.title} is now locked!'

# available for: admin, user - requires authentication token
# @topics_router.put('/{topic_id}/replies')
# def add_replies(topic_id: int, replies_ids: set[int]):
#     if not topic_service.exists(topic_id):
#         return Response(status_code=404)

#     current_ids = topic_service.get_topic_replies(topic_id)
#     replies_to_add = replies_ids.difference(current_ids)

#     if len(replies_to_add) == 0:
#         return {'added_replies_ids': []}

#     topic_service.insert_replies_to_topic(topic_id, replies_to_add)

#     return {'added_replies_ids': replies_to_add}


# available for: admin, user - requires authentication token
# @topics_router.delete('/{topic_id}/replies')
# def remove_repliess(topic_id: int, replies_ids: set[int]):
#     if not topic_service.exists(topic_id):
#         return Response(status_code=404)

#     current_ids = topic_service.get_topic_replies(topic_id)
#     replies_to_delete = replies_ids.intersection(current_ids)
#     if len(replies_to_delete) == 0:
#         return {'deleted_replies_ids': []}

#     topic_service.remove_replies_from_topic(topic_id, replies_to_delete)

#     return {'deleted_replies_ids': replies_to_delete}