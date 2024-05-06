from fastapi import APIRouter, Response
from pydantic import BaseModel
from data.models import Topic, Reply
from services import topic_service, reply_service, category_service
# from services import category_service

class TopicResponseModel(BaseModel):
    topic: Topic
    replies: list[Reply]


topics_router = APIRouter(prefix='/topics')


# shows a list of all the topics a certain category has 
# available for: admin, user, guest
# pagination - query param - to follow
# Postman: GET
# http://127.0.0.1:8000/topics
# http://127.0.0.1:8000/topics?search=sprint
# http://127.0.0.1:8000/topics?sort=asc&sort_by=title
# http://127.0.0.1:8000/topics?search=sprint&sort=asc&sort_by=title
@topics_router.get('/')  
def get_topics(
    sort: str | None = None,
    sort_by: str | None = None,
    search: str | None = None
):
    result = topic_service.all(search)

    if sort and (sort == 'asc' or sort == 'desc'):
        return topic_service.sort(result, reverse=sort == 'desc', attribute=sort_by)
    else:
        return result

# sets the status of a topic - to follow
# available for: admin
# Postman: GET
# http://127.0.0.1:8000/topics/1
@topics_router.get('/{topic_id}')
def get_topic_by_id(topic_id: int):
    topic = topic_service.get_by_id(topic_id)

    if topic is None:
        return Response(status_code=404)
    else:
        return topic
    
# creates a new topic in a specific category
# available for: admin, user
# Postman: POST
# http://127.0.0.1:8000/topics
# {
#     "topic_id": 5,
#     "title": "F1 Miami GP Lando Norris first victory",
#     "category_id": 2,
#     "user_id": 1,
#     "date_time": "2024-05-06T10:00:00"
# }
# {
#     "topic_id": 6,
#     "title": "F1 Miami GP Highlights",
#     "category_id": 2,
#     "user_id": 1,
#     "date_time": "2024-05-06T12:50:00"
# }
@topics_router.post('/', status_code=201)
def create_topic(topic: Topic):
    if not category_service.category_id_exists(topic.category_id):
        return Response(status_code=400,
                        content=f'Category {topic.category_id} does not exist')

    return topic_service.create(topic)


# shows a single topic and a list of its replies
# available for: admin, user, guest
# @topics_router.get('/{id}')
# def get_topic_by_id(id: int): # in header - add token 
#     topic = topic_service.get_by_id(id)

#     if topic is None:
#         return Response(status_code=404)
#     else:
#         return TopicResponseModel(
#             topic=topic,
#             replies=reply_service.get_by_topic(topic.topic_id))


# adds replies to a specific topic
# available for: admin, user


# removes replies from a specific topic
# available for: admin, user


# deletes a specific topic and all of its replies
# available for: admin, user
# Postman: DELETE
# http://127.0.0.1:8000/topics/6
@topics_router.delete('/{topic_id}')
def delete_topic(topic_id: int):
    topic_service.delete(topic_id)

    return Response(status_code=204)