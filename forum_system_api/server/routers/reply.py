# Elena
from fastapi import APIRouter, Response
from data.models import Reply, UpdateReply


replies_router = APIRouter(prefix='/topics')

# TO DO: implement endpoint which will create a new reply
@replies_router.post('/', status_code=201)
def cerate_reply():
       pass

# TO DO: implement endpoint which will upvote/downvote a reply
@replies_router.put()
def get_topic_by_id():
        pass

# TO DO: implement endpoint which will mark a reply as the best one
@replies_router.put()
def create_topic():
    pass