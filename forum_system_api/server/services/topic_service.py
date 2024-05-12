from data.models import Topic, User, TopicUpdate, Reply
from data.database import read_query, insert_query, update_query
from datetime import datetime


def all(search: str = None):
    if search is None:
        data = read_query(
            '''SELECT topic_id, title, date_time, category_id, user_id, best_reply, is_locked
                   FROM topics''')
    else:
        data = read_query(
            '''SELECT topic_id, title, date_time, category_id, user_id, best_reply, is_locked FROM topics 
                   WHERE title LIKE ?''',
        (f'%{search}%',))

    topics_data = []
    for row in data:
        topic = Topic.from_query_result(*row)
        topic.date_time = topic.date_time.strftime('%Y/%m/%d %H:%M')
        topics_data.append(topic)

    return topics_data


def sort(topics: list[Topic], *, attribute='date_time', reverse=False):
    if attribute == 'date_time':
        def sort_fn(t: Topic): return t.date_time
    elif attribute == 'title':
        def sort_fn(t: Topic): return t.title

    return sorted(topics, key=sort_fn, reverse=reverse)


def get_by_id(topic_id: int):
    data = read_query(
        '''SELECT topic_id, title, date_time, category_id, user_id, best_reply, is_locked 
               FROM topics WHERE topic_id = ?''', 
        (topic_id,))
    
    topic = next((Topic.from_query_result(*row) for row in data), None)
    
    if topic:
        topic.date_time = topic.date_time.strftime('%Y/%m/%d %H:%M')
    
    return topic


def create(topic: Topic, user: User):
    generated_id = insert_query(
        '''INSERT INTO topics(topic_id, title, date_time, category_id, user_id, best_reply, is_locked) 
               VALUES(?,?,?,?,?,?,?)''',
        (topic.topic_id, topic.title, topic.date_time, topic.category_id, user.id, topic.best_reply,
                    0 if topic.is_locked == "unlocked" else 1))

    topic.topic_id = generated_id

    return topic

def update(topic_update: TopicUpdate, topic: Topic):
    result = update_query('''UPDATE topics SET best_reply = ? 
                                 WHERE topic_id = ?''',
                          (topic_update.best_reply, topic.topic_id))
    
    topic_result_id = read_query(
        '''SELECT topic_id
               FROM topics WHERE topic_id = ?''', 
        (topic.topic_id,))

    reply_result_id = read_query(
        '''SELECT topic_id
               FROM replies WHERE reply_id = ?''',
        (topic_update.reply_id,))

    if result and topic_result_id == reply_result_id:
        topic.best_reply= topic_update.best_reply
        return topic
    else:
        return f'You cannot choose a best reply from another topic.'
    

def delete(topic: Topic):
    update_query('''DELETE FROM topics 
                        WHERE topic_id = ?''', 
                 (topic.topic_id,))
    

def lock_topic(topic_id: int) -> Topic:
    data = read_query(
                'SELECT topic_id, title, date_time, category_id, user_id, best_reply, is_locked FROM topics WHERE topic_id = ?',
                (topic_id,))

    topic = next((Topic.from_query_result(*row) for row in data), None)
    update_query('UPDATE topics SET is_locked=%s WHERE title = %s',
                 (1, topic.title))

    return topic


def unlock_topic(topic_id: int) -> Topic:
    data = read_query(
                'SELECT topic_id, title, date_time, category_id, user_id, best_reply, is_locked FROM topics WHERE topic_id = ?',
                (topic_id,))

    topic = next((Topic.from_query_result(*row) for row in data), None)
    update_query('UPDATE categories SET is_locked=%s WHERE category_name = %s',
                 (0, topic.title))

    return topic


def topic_id_exists(topic_id: int):
    return any(
        read_query(
                '''SELECT topic_id, title, date_time, category_id, user_id, best_reply, is_locked 
                       FROM topics WHERE topic_id = ?''',
                (topic_id,)))
    
# def get_topic_replies(topic_id: int) -> set[int]:
#     data = read_query(
#         'SELECT topic_id from replies where topic_id = ?',
#         (topic_id,))

#     return set(i[0] for i in data)

# def insert_replies_to_topic(topic_id: int, replies_ids: list[int]):
#     relations = ','.join(
#         f'({topic_id},{reply_id})' for reply_id in replies_ids)

#     insert_query(
#         f'INSERT INTO replies(topic_id, product_id) VALUES {relations}')
    
# def remove_replies_from_topic(topic_id: int, replies_ids: list[int]):
#     ids_to_delete = ','.join(str(r_id) for r_id in replies_ids)

#     insert_query(
#         f'DELETE FROM replies WHERE topic_id = ? and reply_id IN ({ids_to_delete})',
#         (topic_id,))