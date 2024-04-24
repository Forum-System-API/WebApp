from data.database import read_query,update_query,insert_query
from data.models import Category




def all():
    data = read_query('''SELECT category_id, category_name FROM category''')
    return data

def find_by_name(name: str) -> Category | None:
    data = read_query(
        'SELECT category_id, category_name FROM category WHERE name = ?',
        (name,))

    return next((Category.from_query_result(*row) for row in data), None)