from data.database import read_query, update_query, insert_query
from data.models import Category, Topic
from mariadb import IntegrityError


def all():
    data = read_query('SELECT category_id, category_name FROM categories')
    formatted_data = [
        {"category_id": row[0], "category_name": row[1]} for row in data
    ]
    return formatted_data


def find_by_name(category_name: str) -> Category | None:
    data = read_query(
        'SELECT category_id, category_name FROM categories WHERE category_name = ?',
        (category_name,))

    return next((Category.from_query_result(*row) for row in data), None)


def find_by_id(category_id: int) -> tuple[Category | None, list[Topic] | None]:
    category_data = read_query(
        'SELECT category_id, category_name FROM categories WHERE category_id = ?',
        (category_id,))
    topic_data = read_query(
        'SELECT topic_id, title, category_id, user_id, date_time FROM topics WHERE category_id = ?',
        (category_id,))

    category = next((Category.from_query_result(*row) for row in category_data), None)
    topics = [Topic.from_query_result(*row) for row in topic_data]

    return category, topics


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
        'SELECT name FROM categories WHERE name = ?', (name,)
    )

    if existing_category:
        return None

    try:
        generated_id = insert_query(
            'INSERT INTO categories(name) VALUES(?)', (name,))

        return Category(category_id=generated_id, category_name=name)
    except IntegrityError:
        return None

def change_status(category_name: str, is_private: int):
    if is_private == 0:
        is_private_int = 1
    elif is_private == 1:
        is_private_int = 0
    category = read_query(
        '''SELECT name, is_private from categories where name = ? and is_private = ?''', (category_name, is_private_int))

    if category:
        data = category[0]
        name, is_priv = data

    if is_priv != is_private:
        update_query('''UPDATE categories SET is_private=%s WHERE name = %s''',
                     (is_private, category_name))
