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