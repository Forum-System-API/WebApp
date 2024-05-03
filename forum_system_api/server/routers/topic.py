from fastapi import APIRouter, Response
from data.models import Topic
from services import topic_service
from services import category_service


topics_router = APIRouter(prefix='/topics')

# shows a list of all the topics a certain category has - # pagination - query param - to follow
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

# shows a single topic and a list of its replies 
@topics_router.get('/{id}')
def get_topic_by_id(id: int): # in header - add token 
    topic = topic_service.get_by_id(id)

    if topic is None:
        return Response(status_code=404)
    else:
        return topic

# creates a new topic in a specific category
@topics_router.post('/', status_code=201)
def create_topic(topic: Topic):
    if not topic_service.category_exists(topic.category_id):
        return Response(status_code=400,
                        content=f'Category {topic.category_id} does not exist')

    return topic_service.create(topic)

# updates a specific topic
@topics_router.put('/{id}')
def update_topic(id: int, topic: Topic):
    if not topic_service.category_exists(topic.category_id):
        return Response(status_code=400,
                        content=f'Category {topic.category_id} does not exist')

    existing_topic = topic_service.get_by_id(id)
    if existing_topic is None:
        return Response(status_code=404)
    else:
        return topic_service.update(existing_topic, topic)
    

# deletes a specific topic and all of its replies
@topics_router.delete('/{id}')
def delete_topic(id: int):
    topic_service.delete(id)

    return Response(status_code=204)