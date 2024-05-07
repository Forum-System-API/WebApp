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
@topics_router.get('/')  # TO DO: pagination query parameter
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

# available for: admin, user
@topics_router.post('/', status_code=201)
def create_topic(topic: Topic):
    if not category_service.category_id_exists(topic.category_id):
        return Response(status_code=400, content=f'Category {topic.category_id} does not exist')

    return topic_service.create(topic)


# changes the status ofa tipic - locked, private
# available for: admin, user


# adds replies to a specific topic
# available for: admin, user


# removes replies from a specific topic
# available for: admin, user


# available for: admin, user
@topics_router.delete('/{topic_id}')
def delete_topic(topic_id: int):
    topic_service.delete(topic_id)

    return Response(status_code=204)