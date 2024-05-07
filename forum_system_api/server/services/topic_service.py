from data.models import Topic
from data.database import read_query, insert_query, update_query


def all(search: str = None):
    if search is None:
        data = read_query(
            'SELECT topic_id, title, category_id, user_id, date_time FROM topics')
    else:
        data = read_query(
            'SELECT topic_id, title, category_id, user_id, date_time FROM topics WHERE title LIKE ?',
            (f'%{search}%',))

    return (Topic.from_query_result(*row) for row in data)

def sort(topics: list[Topic], *, attribute='date_time', reverse=False):
    if attribute == 'date_time':
        def sort_fn(t: Topic): return t.date_time
    elif attribute == 'title':
        def sort_fn(t: Topic): return t.title
    else:
        def sort_fn(t: Topic): return t.id

    return sorted(topics, key=sort_fn, reverse=reverse)

def get_by_id(topic_id: int):
    data = read_query(
        'SELECT topic_id, title, category_id, user_id, date_time FROM topics WHERE topic_id = ?', 
        (topic_id,))

    return next((Topic.from_query_result(*row) for row in data), None)

def create(topic: Topic):
    generated_id = insert_query(
        'INSERT INTO topics(topic_id, title, category_id, user_id, date_time) VALUES(?,?,?,?,?)',
        (topic.topic_id, topic.title, topic.category_id, topic.user_id, topic.date_time))

    topic.topic_id = generated_id

    return topic

def delete(topic_id: int):
    update_query('DELETE FROM topics WHERE topic_id = ?', 
                 (topic_id,))


def exists(topic_id: int):
    return any(
        read_query(
                'SELECT topic_id, title, category_id, user_id, date_time FROM topics WHERE topic_id = ?',
                (topic_id,)))

def get_topic_replies(topic_id: int) -> set[int]:
    data = read_query(
        'SELECT topic_id from replies where topic_id = ?',
        (topic_id,))

    return set(i[0] for i in data)

def insert_replies_to_topic(topic_id: int, replies_ids: list[int]):
    relations = ','.join(
        f'({topic_id},{reply_id})' for reply_id in replies_ids)

    insert_query(
        f'INSERT INTO replies(topic_id, product_id) VALUES {relations}')
    
def remove_replies_from_topic(topic_id: int, replies_ids: list[int]):
    ids_to_delete = ','.join(str(r_id) for r_id in replies_ids)

    insert_query(
        f'DELETE FROM replies WHERE topic_id = ? and reply_id IN ({ids_to_delete})',
        (topic_id,))