from data.database import read_query, update_query, insert_query
from data.models import Category, Topic, User, Categories_Access
from mariadb import IntegrityError


def detail_view():
    data = read_query(
        'SELECT c.category_id, c.category_name, t.topic_id, t.title FROM categories c '
        'LEFT JOIN topics t ON c.category_id = t.category_id')

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


def all_basic_user(user: User):
    data = read_query(f'''SELECT c.category_id, c.category_name FROM categories_access ca 
                      JOIN categories c JOIN users u WHERE (c.is_private = 0 AND u.user_id = {user.id}) OR 
                      (c.is_private = 1 AND ca.can_write = 1 AND u.user_id = {user.id}) OR
                      (c.is_private = 1 AND ca.can_read = 1 AND u.user_id = {user.id})''')

    formatted_data = [{"category_id": row[0],
                       "category_name": row[1]} for row in data]

    return formatted_data


def find_by_name(category_name: str):
    category_data = read_query(
        'SELECT category_id, category_name, is_private, is_locked FROM categories WHERE category_name = ?',
        (category_name,))

    category = next((Category.from_query_result(*row) for row in category_data), None)

    topic_data = read_query(
        'SELECT topic_id, title, date_time, category_id, user_id, best_reply, is_locked FROM topics '
        'WHERE category_id = ?',
        (category.category_id,))

    topics = [Topic.from_query_result(*row) for row in topic_data]

    return category, topics


def find_by_id(category_id: int):
    category_data = read_query(
        'SELECT category_id, category_name, is_private, is_locked FROM categories WHERE category_id = ?',
        (category_id,))

    category = next((Category.from_query_result(*row) for row in category_data), None)

    topic_data = read_query(
        'SELECT topic_id, title, date_time, category_id, user_id, best_reply, is_locked FROM topics WHERE category_id = ?',
        (category_id,))

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


def lock_unlock_category(category_name: str, is_locked: int):
    if is_locked == 0:
        is_locked_int = 1
    elif is_locked == 1:
        is_locked_int = 0
    category = read_query(
        '''SELECT category_name, is_locked FROM categories WHERE category_name = ? and is_locked = ?''',
        (category_name, is_locked_int))

    if category:
        data = category[0]
        name, is_lck = data

    if is_lck != is_locked:
        update_query('''UPDATE categories SET is_locked=%s WHERE category_name = %s''',
                     (is_locked, category_name))


def grab_category_with_id(category_id: int) -> Category:
    category_data = read_query(
        'SELECT category_id, category_name, is_private, is_locked FROM categories WHERE category_id = ?',
        (category_id,))

    return next((Category.from_query_result(*row) for row in category_data), None)


def grab_category_with_name(category_name: str) -> Category:
    category_data = read_query(
        'SELECT category_id, category_name, is_private, is_locked FROM categories WHERE category_name = ?',
        (category_name,))

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


def delete_category(name: str, is_private: int, is_locked: int):
    update_query('DELETE FROM categories WHERE category_name = ?', (name,))
    return "Category deleted!"


def create(name: str, is_private:int, is_locked:int):
    existing_category = read_query(
        'SELECT category_name FROM categories WHERE category_name = ?', (name,)
    )

    if existing_category:
        return None

    try:
        insert_query(
            'INSERT INTO categories(category_name, is_private, is_locked) VALUES(?,?,?)', (name, is_private, is_locked))

        return Category(category_name=name, is_private=is_private, is_locked=is_locked)
    except IntegrityError:
        return None


def change_status(category_name: str, is_private: int):
    if is_private == 0:
        is_private_int = 1
    elif is_private == 1:
        is_private_int = 0
    category = read_query(
        '''SELECT category_name, is_private FROM categories WHERE category_name = ? and is_private = ?''',
        (category_name, is_private_int))

    if category:
        data = category[0]
        name, is_priv = data

    if is_priv != is_private:
        update_query('''UPDATE categories SET is_private=%s WHERE category_name = %s''',
                     (is_private, category_name))


def read_access(categories_access):
    test_data = read_query('SELECT user_id, category_id FROM categories_access')
    if not test_data:
        data_insert = insert_query(
            f'INSERT INTO categories_access (user_id, category_id, can_read, can_write)'
            f' VALUES ({categories_access.user_id}, {categories_access.category_id}, '
            f'{categories_access.can_read}, {categories_access.can_write})')
        return data_insert
    else:
        data_update = update_query('UPDATE categories_access SET can_read=?, can_write=? '
                                   'WHERE user_id=? AND category_id=?',
                                   (categories_access.can_read, categories_access.can_write, categories_access.user_id,
                                    categories_access.category_id))
        return data_update


def check_privacy(user_id: int):
    data = read_query('''SELECT ca.category_id FROM categories_access ca
                      JOIN categories c ON ca.category_id = c.category_id
                      WHERE ca.user_id = ? AND c.is_private=1''', (user_id,))

    return len(data) > 0


def get_privileged(category_id: int):
    data = read_query('''SELECT u.username, ca.user_id, ca.can_read, ca.can_write 
    FROM users u
    JOIN categories_access ca ON u.user_id = ca.user_id
    JOIN categories c ON ca.category_id = c.category_id
    WHERE c.category_id = 1''', (category_id,))
    # privileged_data = []
    # for row in data:
    #
    #     pass

    return data[0]
