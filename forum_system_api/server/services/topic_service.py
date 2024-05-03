# from data.models import Topic
# from data.database import insert_query, read_query, update_query


# def all(search: str = None):
#     if search is None:
#         data = read_query(
#             '''SELECT id, title, category_id, user_id, timestamp, best_reply_id
#                FROM topics''')
#     else:
#         data = read_query(
#             '''SELECT id, title, category_id, user_id, timestamp, best_reply_id
#                FROM topics 
#                WHERE title LIKE ?''', (f'%{search}%',))

#     return (Topic.from_query_result(*row) for row in data)

# def sort(topics: list[Topic], *, attribute='title', reverse=False):
#     if attribute == 'title':
#         def sort_fn(t: Topic): return t.title
#     elif attribute == 'timestamp':
#         def sort_fn(t: Topic): return t.timestamp
#     else:
#         def sort_fn(t: Topic): return t.category_id

#     return sorted(topics, key=sort_fn, reverse=reverse)

# def get_by_id(id: int):
#     data = read_query(
#         '''SELECT id, title, category_id, user_id, timestamp, best_reply_id
#             FROM topics 
#             WHERE id = ?''', (id,))

#     return next((Topic.from_query_result(*row) for row in data), None)

# def category_exists(category_id: int) -> bool: # move in categories
#     return any(
#         read_query(
#             'SELECT category_id, name from categories where category_id = ?',
#             (category_id,)))

# def create(topic: Topic):
#     generated_id = insert_query(
#         'INSERT INTO topics(id,title,category_id,user_id,timestamp,best_reply_id) VALUES(?,?,?,?,?,?)',
#         (topic.title, topic.category_id, topic.user_id, topic.timestamp, topic.best_reply_id))

#     topic.id = generated_id

#     return topic

# def update(old: Topic, new: Topic):
#     merged = Topic(
#         id=old.id,
#         title=new.title or old.title,
#         category_id=new.category_id or old.category_id,
#         user_id=old.user_id,
#         timestamp=old.timestamp,
#         best_reply_id=new.best_reply_id or old.best_reply_id)

#     update_query(
#         '''UPDATE topics SET
#            title = ?, category_id = ?, best_reply_id = ?
#            WHERE id = ? 
#         ''',
#         (merged.id, merged.title, merged.category_id, merged.user_id, merged.timestamp, merged.best_reply_id))

#     return merged

# def remove_reply_from_topic():
#     pass

# def delete(topic_id):
#     update_query('DELETE FROM topics WHERE id = ?', (topic_id,))

