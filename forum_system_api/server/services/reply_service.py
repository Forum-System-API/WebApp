from data.database import insert_query, read_query, update_query
from data.models import Reply, Topic


def get_by_topic(topic_id: int):
    data = read_query(
        '''SELECT topic_id, title, category_id, user_id, date_time
            FROM topics
            WHERE topic_id = ?''', (topic_id,))

    return (Topic.from_query_result(*row) for row in data)

# def get_by_id(id: int):
#     data = read_query(
#         '''SELECT reply_id, text, upvotes, downvotes, topic_id, user_id, timestamp
#             FROM replies 
#             WHERE reply_id = ?''', (id,))

#     return next((Reply.from_query_result(*row) for row in data), None)

# def topic_exists(topic_id: int) -> bool:
#     return any(
#         read_query(
#             'SELECT topic_id, title from topics where topic_id = ?',
#             (topic_id,)))

# def create(reply: Reply):
#     generated_id = insert_query(
#         'INSERT INTO replies(text,upvotes,downvotes,topic_id,user_id,timestamp) VALUES(?,?,?,?,?,?)',
#         (reply.text, reply.upvotes, reply.downvotes, reply.topic_id, reply.user_id, reply.timestamp))

#     reply.id = generated_id

#     # add_replies_to_topic(reply.id, reply.topic_id)

#     return reply

# # def add_replies_to_topic():
# #     pass

# def update(old: Reply, new: Reply):
#     merged = Reply(
#         id=old.id,
#         text=new.text or old.text,
#         upvotes=old.upvotes,
#         downvotes=old.downvotes,
#         topic_id=old.topic_id,
#         user_id=old.user_id,
#         timestamp=old.timestamp)

#     update_query(
#         '''UPDATE replies SET
#            text = ?
#            WHERE id = ? 
#         ''',
#         (merged.id, merged.text, merged.upvotes, merged.downvotes, merged.topic_id, merged.user_id, merged.timestamp))

#     return merged


# def delete(reply_id):
#     update_query('DELETE FROM replies WHERE id = ?', (reply_id,))


