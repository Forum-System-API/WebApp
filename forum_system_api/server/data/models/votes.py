from datetime import datetime
from pydantic import BaseModel, constr


class VoteTypes:
    INT_TO_STR = {0:'upvote', 1:'downvote'}
    STR_TO_INT = {'upvote':0, 'downvote':1}

class Vote(BaseModel):
    reply_id: int | None = None
    user_id: int | None = None
    type_of_vote: constr(pattern='^upvote|downvote$')

    @classmethod
    def from_query_result(cls, reply_id, user_id, type_of_vote):
        return cls(
            reply_id=reply_id,
            user_id=user_id,
            type_of_vote=VoteTypes.INT_TO_STR[type_of_vote]
            )