from data.database import read_query, update_query, insert_query
from data.models import Category, Topic
from mariadb import IntegrityError


def detail_view():
    data = read_query(
        'SELECT c.category_id, c.category_name, t.topic_id, t.title FROM categories c LEFT JOIN topics t ON c.category_id = t.category_id')

    categories = {}
    for row in data:
        category_id, category_name, topic_id, topic_title = row
        if category_id not in categories:
            categories[category_id] = {
                "category_id": category_id, "category_name": category_name, "topics": []}
        if topic_id:
            categories[category_id]["topics"].append(
                {"topic_id": topic_id, "title": topic_title})

    return list(categories.values())


def all_basic_user():
    data = read_query(
        'SELECT category_id, category_name, is_private FROM categories where is_private!=1')
    # is_private_data = read_query('SELECT is_private FROM categories')
    # if is_private_data == 1:
    formatted_data = [{"category_id": row[0],
                       "category_name": row[1], "is_private": row[2]} for row in data]

    return formatted_data


def find_by_name(category_name: str):
    category_data = read_query(
        'SELECT category_id, category_name, is_private, is_locked FROM categories WHERE category_name = ?',
        (category_name,))

    category = next((Category.from_query_result(*row) for row in category_data), None)

    topic_data = read_query(
        'SELECT topic_id, title, category_id, user_id, date_time FROM topics WHERE category_id = ?',
        (category.category_id,))

    topics = [Topic.from_query_result(*row) for row in topic_data]

    return category, topics


def find_by_id(category_id: int) -> tuple[Category | None, list[Topic] | None]:
    category_data = read_query(
        'SELECT category_id, category_name, is_private, is_locked FROM categories WHERE category_id = ?',
        (category_id,))
    topic_data = read_query(
        'SELECT topic_id, title, category_id, user_id, date_time FROM topics WHERE category_id = ?',
        (category_id,))

    category = next((Category.from_query_result(*row) for row in category_data), None)
    topics = [Topic.from_query_result(*row) for row in topic_data]

    return category, topics


def lock_category(category_id: int) -> Category:
    category_data = read_query(
        'SELECT category_id, category_name, is_private, is_locked FROM categories WHERE category_id = ?',
        (category_id,))

    category = next((Category.from_query_result(*row) for row in category_data), None)
    update_query('''UPDATE categories SET is_locked=%s WHERE category_name = %s''',
                 (1, category.category_name))

    return category


def unlock_category(category_id: int) -> Category:
    category_data = read_query(
        'SELECT category_id, category_name, is_private, is_locked FROM categories WHERE category_id = ?',
        (category_id,))

    category = next((Category.from_query_result(*row) for row in category_data), None)
    update_query('''UPDATE categories SET is_locked=%s WHERE category_name = %s''',
                 (0, category.category_name))

    return category


def grab_category_with_id(category_id: int) -> Category:
    category_data = read_query(
        'SELECT category_id, category_name FROM categories WHERE category_id = ?',
        (category_id,))

    return next((Category.from_query_result(*row) for row in category_data), None)


def category_name_exists(category_name: str) -> bool:
    return any(
        read_query(
            'SELECT category_id, category_name FROM categories WHERE category_name = ?',
            (category_name,)))


def category_id_exists(category_id: int) -> bool:
    return any(
        read_query(
            'SELECT category_id, category_name FROM categories WHERE category_id = ?',
            (category_id,)))


def delete_category(name):  #Untested
    update_query(f'DELETE FROM categories WHERE categories.name = {name}')


def create(name: str):
    existing_category = read_query(
        'SELECT category_name FROM categories WHERE name = ?', (name,)
    )

    if existing_category:
        return None

    try:
        generated_id = insert_query(
            'INSERT INTO categories(category_name) VALUES(?)', (name,))

        return Category(category_id=generated_id, category_name=name)
    except IntegrityError:
        return None


def change_status(category_name: str, is_private: int):
    if is_private == 0:
        is_private_int = 1
    elif is_private == 1:
        is_private_int = 0
    category = read_query(
        '''SELECT name, is_private from categories where name = ? and is_private = ?''',
        (category_name, is_private_int))

    if category:
        data = category[0]
        name, is_priv = data

    if is_priv != is_private:
        update_query('''UPDATE categories SET is_private=%s WHERE name = %s''',
                     (is_private, category_name))

def read_access(Categories_Access):
    data = insert_query(
        f'INSERT INTO categories_access (user_id, category_id, can_read, can_write)'
        f' VALUES ({Categories_Access.user_id}, {Categories_Access.category_id}, '
        f'{Categories_Access.can_read}, {Categories_Access.can_write})')
    return data

def check_privacy(user_id:int):
    data = read_query('''SELECT ca.category_id from categories_access ca
                      JOIN categories c ON ca.category_id = c.category_id
                      WHERE ca.user_id = ? AND c.is_private=1''',(user_id,))
    
    return len(data) > 0
