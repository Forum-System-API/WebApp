from fastapi import APIRouter, Response
# from fastapi_pagination import Page, paginate
from pydantic import BaseModel
from data.models import Topic, Reply
from services import topic_service, reply_service, category_service


class TopicResponseModel(BaseModel):
    topic: Topic
    replies: list[Reply]

topics_router = APIRouter(prefix='/topics')

# available for: admin, user, guest
# TO DO: pagination query parameter
@topics_router.get('/') 
def get_topics(sort: str | None = None, sort_by: str | None = None, search: str | None = None):
    result = topic_service.all(search)

    if sort and (sort == 'asc' or sort == 'desc'):
        return topic_service.sort(result, reverse=sort == 'desc', attribute=sort_by)
    else:
        return result

# available for: admin, user, guest
@topics_router.get('/{topic_id}')
def get_topic_by_id(topic_id: int):
    topic = topic_service.get_by_id(topic_id)

    if topic is None:
        return Response(status_code=404)
    else:
        return TopicResponseModel(topic=topic, replies=reply_service.get_by_topic(topic.topic_id))

# available for: admin, user - requires authentication token
@topics_router.post('/', status_code=201)
def create_topic(topic: Topic):
    if not category_service.category_id_exists(topic.category_id):
        return Response(status_code=400, content=f'Category {topic.category_id} does not exist')

    return topic_service.create(topic)


# changes the status of a tоpic - best reply
# available for: admin, user - requires authentication token


# changes the status of a tоpic - private
# available for: admin, user - requires authentication token


# changes the status of a tоpic - locked
# available for: admin, user - requires authentication token


# available for: admin, user - requires authentication token
@topics_router.put('/{topic_id}/replies')
def add_replies(topic_id: int, replies_ids: set[int]):
    if not topic_service.exists(topic_id):
        return Response(status_code=404)

    current_ids = topic_service.get_topic_replies(topic_id)
    replies_to_add = replies_ids.difference(current_ids)

    if len(replies_to_add) == 0:
        return {'added_replies_ids': []}

    topic_service.insert_replies_to_topic(topic_id, replies_to_add)

    return {'added_replies_ids': replies_to_add}

# available for: admin, user - requires authentication token
@topics_router.delete('/{topic_id}/replies')
def remove_repliess(topic_id: int, replies_ids: set[int]):
    if not topic_service.exists(topic_id):
        return Response(status_code=404)

    current_ids = topic_service.get_topic_replies(topic_id)
    replies_to_delete = replies_ids.intersection(current_ids)
    if len(replies_to_delete) == 0:
        return {'deleted_replies_ids': []}

    topic_service.remove_replies_from_topic(topic_id, replies_to_delete)

    return {'deleted_replies_ids': replies_to_delete}

# available for: admin, user - requires authentication token
@topics_router.delete('/{topic_id}')
def delete_topic(topic_id: int):
    topic_service.delete(topic_id)

    return Response(status_code=204)