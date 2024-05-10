from data.database import insert_query, read_query, update_query
from data.models import Reply, User, ReplyUpdate

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
    data = read_query(
        'SELECT reply_id, text, date_time, topic_id, user_id FROM replies WHERE reply_id = ?''',
        (reply_id,))

    return next((Reply.from_query_result(*row) for row in data), None)


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