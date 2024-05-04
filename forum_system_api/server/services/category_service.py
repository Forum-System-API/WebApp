from data.database import read_query, update_query, insert_query
from data.models import Category


def all():
    data = read_query('SELECT category_id, category_name FROM categories')
    return data


def find_by_name(category_name: str) -> Category | None:
    data = read_query(
        'SELECT category_id, category_name FROM categories WHERE category_name = ?',
        (category_name,))

    return next((Category.from_query_result(*row) for row in data), None)


def find_by_id(category_id: int) -> Category | None:
    data = read_query(
        'SELECT category_id, category_name FROM categories WHERE category_id = ?',
        (category_id,))

    return next((Category.from_query_result(*row) for row in data), None)


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
