from fastapi import APIRouter, Response, status, HTTPException, Header
from data.models import Category, Role, User
from services import category_service
from common.auth import get_user_or_raise_401

category_router = APIRouter(prefix='/categories')


@category_router.get('/')
def show_categories():
    categories = category_service.show_all()
    return categories


@category_router.get('/name/{name}')
def show_category_by_name(name: str):
    if not category_service.category_name_exists(name):
        return Response(status_code=400,
                        content=f'Category with name "{name}" does not exist')

    category = category_service.find_by_name(name)
    return category


@category_router.get('/id/{category_id}')
def show_category_by_id(category_id: int):
    if not category_service.category_id_exists(category_id):
        return Response(status_code=400,
                        content=f'Category with id #{category_id} does not exist')

    category = category_service.find_by_id(category_id)
    return category


@category_router.put('/lock/{category_id}')
def show_category_by_id(category_id: int, x_token=Header()):
    logged_user = get_user_or_raise_401(x_token)
    if logged_user.role != "admin":
        return Response(status_code=400,
                        content=f'You need administrative rights to lock categories!')
    if not category_service.category_id_exists(category_id):
        return Response(status_code=400,
                        content=f'Category with id #{category_id} does not exist')

    category = category_service.lock_category(category_id)
    return f"Category {category.category_name} with id #{category.category_id} is now locked!"


@category_router.put('/unlock/{category_id}')
def show_category_by_id(category_id: int, x_token=Header()):
    logged_user = get_user_or_raise_401(x_token)
    if logged_user.role != "admin":
        return Response(status_code=400,
                        content=f'You need administrative rights to unlock categories!')
    if not category_service.category_id_exists(category_id):
        return Response(status_code=400,
                        content=f'Category with id #{category_id} does not exist')

    category = category_service.unlock_category(category_id)
    return f"Category {category.category_name} with id #{category.category_id} is now unlocked!"


@category_router.delete('/{category_id}')
def delete_category_by_id(category_id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not category_service.category_id_exists(category_id):
        return Response(status_code=400,
                        content=f'Category with id #{category_id} does not exist')

    if not user.role != "admin":
        return Response(status_code=403,
                        content=f'You need administrative rights to delete categories!')

    category = category_service.grab_category_with_id(category_id)
    category_service.delete_category(category.category_name)


@category_router.delete('/{name}')
def delete_category_by_name(name: str, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not category_service.category_name_exists(name):
        return Response(status_code=400,
                        content=f'Category with id #{name} does not exist')

    if not user.role != "admin":
        return Response(status_code=403,
                        content=f'You need administrative rights to delete categories!')

    category_service.delete_category(name)



@category_router.post('/new')
def create_category(category: Category, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    id, username = x_token.split(';')

    if user.role != Role.ADMIN and username != 'admin':
        raise HTTPException(status_code=403, detail="Admin credentials are required for this option!")

    category_service.create(category.category_name)

    return f'Category created successfully!'


@category_router.post('/visibility')
def set_privacy(category: Category, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)  ## to finish the logic

    id, username = x_token.split(';')

    if user.role != Role.ADMIN and username != 'admin':
        raise HTTPException(status_code=403, detail="Admin credentials are required for this option!")

    category_service.change_status(category.category_name, category.is_private)

    return {"message": "Category privacy updated successfully"}
