from fastapi import APIRouter, Header
from common.responses import NotFound, BadRequest, InternalServerError, Unauthorized, NoContent
from common.auth import get_user_or_raise_401
from data.models import Reply, ReplyUpdate, Vote
from services import reply_service, topic_service, user_service
from datetime import datetime

replies_router = APIRouter(prefix='/replies')


@replies_router.post('/')
def create_reply(reply: Reply, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if not topic_service.topic_id_exists(reply.topic_id):
        return BadRequest(content=f'Topic {reply.topic_id} does not exist.')  # status_code=400

    if reply_service.is_locked(reply.topic_id):
        return BadRequest(content=f'This topic is locked  and you can\'t add replies.')

    reply_topic = topic_service.get_by_id(user=user, topic_id=reply.topic_id)
    category_topic = reply_topic.category_id

    access = topic_service.has_topic_write_access(category_topic, user)

    if access:
        reply.date_time = datetime.now()
        reply.date_time = reply.date_time.strftime('%Y/%m/%d %H:%M')

        return reply_service.create(reply, user)


@replies_router.put('/{reply_id}')
def update_reply(reply_id: int, data: ReplyUpdate, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

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


@replies_router.delete('/{reply_id}')
def delete_reply(reply_id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    reply = reply_service.get_by_id(reply_id)
    if reply is None:
        return NotFound()  # status_code=404

    if not user_service.owns_reply(user, reply):
        return Unauthorized('Can`t edit others` replies.')  # status_code=401

    reply_service.delete(reply)

    return NoContent()  # status_code=204


@replies_router.post('/id/{reply_id}')
def vote_reply(reply_id: int, vote: Vote, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not user:
        return Unauthorized()  # status_code=401

    if vote.type_of_vote not in ['upvote', 'downvote']:
        return BadRequest(content=f'{vote.type_of_vote} invalid vote type.')

    vote.reply_id, vote.user_id = reply_id, user.id
    reply = reply_service.get_by_id(reply_id)
    if reply is None:
        return NotFound()  # status_code=404

    this_topic = topic_service.get_by_id(topic_id=reply.topic_id, user=user)

    if reply_service.has_access(this_topic.category_id, user):
        existing_vote = reply_service.get_vote(vote=vote)
        if existing_vote:
            if existing_vote == vote.type_of_vote:
                return BadRequest(content=f'You have already voted.')  # status_code=400
            else:
                existing_vote = vote.type_of_vote
                reply_service.update_reply_vote(existing_vote=existing_vote, reply_id=reply_id, vote=vote)
                return {'Message': 'You have changed your vote successfully.'}

        reply_service.create_vote(reply_id, vote)
        return {'Message': 'You have voted successfully.'}
    return 'You cannot vote as the topic is locked.'


@replies_router.put('/id/{reply_id}/votes')
def vote_reply(reply_id: int, vote: Vote, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if not user:
        return Unauthorized()  # status_code=401

    if vote.type_of_vote not in ['upvote', 'downvote']:
        return BadRequest(content=f'{vote.type_of_vote} invalid vote type.')  # status_code=400

    existing_vote = reply_service.get_vote(vote=vote)
    if existing_vote:
        if existing_vote == vote.type_of_vote:
            return BadRequest(content=f'You have already voted.')  # status_code=400
        else:
            existing_vote = vote.type_of_vote
            reply_service.update_reply_vote(existing_vote=existing_vote, reply_id=reply_id, vote=vote)
            return existing_vote

    updated_reply = existing_vote
    return updated_reply


@replies_router.get('/{reply_id}')
def get_reply_by_id(reply_id: int):
    reply = reply_service.get_by_id_with_votes(reply_id)

    if reply is None:
        return NotFound()
    else:
        return reply
