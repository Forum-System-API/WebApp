from datetime import datetime
from pydantic import BaseModel, constr


class Category(BaseModel): 
    category_id: int | None = None
    category_name: str
    is_private: int = 0
    is_locked: int = 0

    @classmethod
    def from_query_result(cls, category_id, category_name, is_private, is_locked):
        return cls(
            category_id=category_id,
            category_name=category_name,
            is_private = is_private,
            is_locked = is_locked
        )


class Categories_Access(BaseModel):
    user_id: int
    category_id: int
    can_read: int = 1
    can_write: int = 1
