from data.database import insert_query, read_query, update_query
from data.models import Reply, Topic

def create(reply: Reply):
    generated_id = insert_query(
        'INSERT INTO replies(reply_id, text, date_time, topic_id, user_id) VALUES(?,?,?,?,?)',
        (reply.reply_id, reply.text, reply.date_time, reply.topic_id, reply.user_id))

    reply.reply_id = generated_id

    return reply

def get_by_id(reply_id: int):
    data = read_query(
        'SELECT reply_id, text, date_time, topic_id, user_id FROM replies WHERE reply_id = ?''',
        (reply_id,))

    return next((Reply.from_query_result(*row) for row in data), None)

def update(old: Reply, new: Reply):
    merged = Reply(reply_id=old.reply_id, text=new.text or old.text, topic_id=old.topic_id, user_id=old.user_id, date_time=old.date_time)

    update_query(
        'UPDATE replies SET text = ? WHERE reply_id = ?',
        (merged.reply_id, merged.text, merged.topic_id, merged.user_id, merged.date_time))

    return merged

def get_by_topic(topic_id: int):
    data = read_query(
        'SELECT topic_id, title, category_id, user_id, date_time FROM topics WHERE topic_id = ?',
        (topic_id,))

    return (Topic.from_query_result(*row) for row in data)

def delete(reply_id: int):
    update_query('DELETE FROM replies WHERE reply_id = ?', 
                 (reply_id,))