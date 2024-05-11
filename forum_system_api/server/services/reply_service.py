from data.database import insert_query, read_query, update_query
from data.models import Reply, User, ReplyUpdate, Vote, VoteTypes


def create(reply: Reply, user: User):
    generated_id = insert_query(
        'INSERT INTO replies(reply_id, text, date_time, topic_id, user_id) VALUES(?,?,?,?,?)',
        (reply.reply_id, reply.text, reply.date_time, reply.topic_id, user.id))

    reply.reply_id = generated_id

    return reply

def reply_id_exists(reply_id: int):
    return any(
        read_query(
                'SELECT reply_id, text, date_time, topic_id, user_id FROM replies WHERE reply_id = ?',
                (reply_id,)))


def get_by_id(reply_id: int):
    reply_data = read_query(
        'SELECT reply_id, text, date_time, topic_id, user_id FROM replies WHERE reply_id = ?',
        (reply_id,))
    
    votes_data = read_query(
        'SELECT reply_id, user_id, type_of_vote FROM votes WHERE reply_id = ?',
        (reply_id,))
    
    reply_result = next((Reply.from_query_result(*row) for row in reply_data), None)
    vote_result = next((Vote.from_query_result(*row) for row in votes_data), None)

    return reply_result, vote_result


def update(reply_update: ReplyUpdate, reply: Reply):
    result = update_query('UPDATE replies SET text = ? WHERE reply_id = ?',
        (reply_update.text, reply.reply_id))

    if result:
        reply.text= reply_update.text
        return reply
    else:
        return None


def get_by_topic(topic_id: int):
    data = read_query(
        'SELECT reply_id, text, date_time, topic_id, user_id FROM replies WHERE topic_id = ?',
        (topic_id,))

    return (Reply.from_query_result(*row) for row in data)


def delete(reply: Reply):
    update_query('DELETE FROM replies WHERE reply_id = ?', 
                 (reply.reply_id,))
    
    
def get_vote(reply_id: int):
    data = read_query(
        'SELECT reply_id, user_id, type_of_vote FROM votes WHERE reply_id = ?',
        (reply_id,))

    return (Vote.from_query_result(*row) for row in data)


def update_reply_vote(reply_id: int, vote: Vote):
    existing_vote = read_query(
        'SELECT reply_id, user_id, type_of_vote FROM votes WHERE reply_id = ?',
        (reply_id,))

    if not existing_vote:
        existing_vote.type_of_vote = VoteTypes.STR_TO_INT[vote.type_of_vote]
        existing_vote = insert_query(
        'INSERT INTO votes(reply_id, user_id, type_of_vote) VALUES(?,?,?)',
        (vote.reply_id, vote.user_id, vote.type_of_vote))
    else:
        existing_vote.type_of_vote = VoteTypes.STR_TO_INT[vote.type_of_vote]
        existing_vote = insert_query(
        'UPDATE votes SET user_id = ?, type_of_vote = ? WHERE reply_id = ?)',
        (vote.user_id, vote.type_of_vote))

        return existing_vote
