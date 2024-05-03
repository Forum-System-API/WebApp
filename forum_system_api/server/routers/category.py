from fastapi import APIRouter, Response, status, HTTPException, Header
from data.models import Category
from services import category_service
from common.auth import get_user_or_raise_401

category_router = APIRouter(prefix='/categories')


@category_router.get("/")
def show_categories():
    categories = category_service.all()


@category_router.get("/{category_name}")
def show_category_by_name(category_name: str):
    if not category_service.category_name_exists(category_name):
        return Response(status_code=400,
                        content=f'Category with name "{category_name}" does not exist')

    category = category_service.find_by_name(category_name)
    return category


@category_router.get("/{category_id}")
def show_category_by_id(category_id: int):
    if not category_service.category_id_exists(category_id):
        return Response(status_code=400,
                        content=f'Category with id #{category_id} does not exist')

    category = category_service.find_by_id(category_id)
    return category


@category_router.delete("/{category_id}")
def delete_category_by_id(category_id: int, x_token: str = Header()):
    #user = get_user_or_raise_401(x_token)
    if not category_service.category_id_exists(category_id):
        return Response(status_code=400,
                        content=f'Category with id #{category_id} does not exist')

    #if not user.role != "admin":
        #pass
    pass


@category_router.delete("/{category_name}")
def delete_category_by_id(category_name: str, x_token: str = Header()):
    #user = get_user_or_raise_401(x_token)
    if not category_service.category_name_exists(category_name):
        return Response(status_code=400,
                        content=f'Category with id #{category_name} does not exist')

    #if not user.role != "admin":
        #pass
    pass