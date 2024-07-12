from fastapi import APIRouter, Response, status, HTTPException, Header, Query
from data.models.categories import Category, Categories_Access
from data.models.users import Role, User
from services import category_service, topic_service
from common.auth import get_user_or_raise_401


category_router = APIRouter(prefix='/categories', tags = ['categories'])


@category_router.get('/')
def show_categories(x_token: str = Header()):
    '''
    Retrieve categories with role-based access.

    This endpoint fetches categories based on the user's role. Admin users receive detailed categories, while ordinary users receive basic categories.
    '''
    user = get_user_or_raise_401(x_token)

    if user.role == Role.ADMIN:
        categories = category_service.detail_view()
        return categories

    categories = category_service.all_basic_user(user)
    return categories


@category_router.get('/name/{category_name}')
def show_category_by_name(category_name: str, x_token=Header()):
    '''
    Retrieve category details by name.

    This endpoint fetches a category by its name, considering the user's access rights. 
    Admin users can access all categories, 
    while other users need specific access to private categories.
    '''
    user = get_user_or_raise_401(x_token)

    if not category_service.category_name_exists(category_name):
        return Response(status_code=400,
                        content=f'Category with name "{category_name}" does not exist')

    category = category_service.grab_category_with_name(category_name)
    category_access = category_service.check_privacy(user.id, category.category_id)

    if category.is_private == 1 and user.role != Role.ADMIN:
        if not category_access:
            return Response(status_code=403,
                            content='You do not have category access rights')

    category = category_service.find_by_name(category_name)
    return category


@category_router.get('/id/{category_id}')
def show_category_by_id(category_id: int, x_token=Header()):
    '''
    Retrieve category details by ID.

    This endpoint fetches a category by its ID, considering the user's access rights. 
    Admin users can access all categories, while other users need specific access to private categories.
    '''
    user = get_user_or_raise_401(x_token)

    if not category_service.category_id_exists(category_id):
        return Response(status_code=400,
                        content=f'Category with id #{category_id} does not exist')

    category = category_service.grab_category_with_id(category_id)
    category_access = category_service.check_privacy(user.id, category_id)

    if category.is_private == 1 and user.role != Role.ADMIN:
        if not category_access:
            return Response(status_code=403,
                            content='You do not have category access rights')

    category = category_service.find_by_id(category_id)
    return category


@category_router.put('/lock')
def show_category_by_id(category: Category, x_token=Header()):
    '''
    Lock or unlock a category.

    This endpoint allows an admin user to lock or unlock a category. 
    It verifies the user's role and the current status of the category before updating.
    '''
    user = get_user_or_raise_401(x_token)
    current_category = category_service.grab_category_with_name(category.category_name)
    current_status = current_category.is_locked

    if user.role != "admin":
        return Response(status_code=400,
                        content=f'You need administrative rights to lock/unlock categories!')
    if not category_service.category_id_exists(current_category.category_id):
        return Response(status_code=400,
                        content=f'Category with id #{current_category.category_id} does not exist')

    if category.is_locked == 1:
        category_status = "locked"
    else:
        category_status = "unlocked"
    if category.is_locked == current_status:
        return f"The status of category {current_category.category_name} is already {category_status}!"

    category_service.lock_unlock_category(current_category.category_name, category.is_locked)
    return f"Category {current_category.category_name} with id #{current_category.category_id} is now {category_status}!"


@category_router.delete('/{category_id}')
def delete_category_by_id(category_id: int, x_token: str = Header()):
    '''
    Delete a category by ID.

    This endpoint allows an admin user to delete a category by its ID. 
    It verifies the user's role and checks if the category exists before deleting.
    '''
    user = get_user_or_raise_401(x_token)
    if not category_service.category_id_exists(category_id):
        return Response(status_code=400,
                        content=f'Category with id #{category_id} does not exist')

    if not user.role != "admin":
        return Response(status_code=403,
                        content=f'You need administrative rights to delete categories!')

    category = category_service.grab_category_with_id(category_id)
    category_service.delete_category(category.category_name)


@category_router.delete('/')
def delete_category_by_name(category: Category, x_token: str = Header()):
    '''
    Delete a category by name.

    This endpoint allows an admin user to delete a category by its name. 
    It verifies the user's role and checks if the category exists before deleting.
    '''
    user = get_user_or_raise_401(x_token)
    if not category_service.category_name_exists(category.category_name):
        return Response(status_code=400,
                        content=f'Category with name {category.category_name} does not exist')

    if user.role != "admin":
        return Response(status_code=403,
                        content=f'You need administrative rights to delete categories!')

    category_service.delete_category(category.category_name, category.is_private, category.is_locked)
    return "Category deleted!"


@category_router.post('/new')
def create_category(category: Category, x_token: str = Header()):
    '''
    Create a new category.

    This endpoint allows an admin user to create a new category. It verifies the user's role based on the token provided and creates the category with the specified properties.
    '''
    user = get_user_or_raise_401(x_token)

    id, username = x_token.split(';')

    if user.role != Role.ADMIN and username != 'admin':
        raise HTTPException(status_code=403, detail="Admin credentials are required for this option!")

    category_service.create(category.category_name, category.is_private, category.is_locked)

    return f'Category created successfully!'


@category_router.put('/privacy')
def set_privacy(category: Category, x_token: str = Header()):
    '''
    Update privacy settings for a category.

    This endpoint allows an admin user to update the 
    privacy settings (public or private) for a category.
    It verifies the user's role based on the token provided 
    and updates the category's privacy status accordingly.
    '''
    user = get_user_or_raise_401(x_token)
    id, username = x_token.split(';')
    get_category = category_service.grab_category_with_name(category.category_name)
    current_status = get_category.is_private

    if user.role != Role.ADMIN and username != 'admin':
        raise HTTPException(status_code=403, detail="Admin credentials are required for this option!")

    if category.is_private == 1:
        category_status = "private"
    else:
        category_status = "public"
    if category.is_private == current_status:
        return f"The status of category {category.category_name} is already {category_status}!"

    category_service.change_status(category.category_name, category.is_private)

    return f"The status of category {category.category_name} updated to {category_status} successfully"


@category_router.post('/membership')
def read_access(access: Categories_Access, x_token: str = Header()):
    '''
    Manage user access rights to a category.

    This endpoint allows an admin user to grant or revoke access rights 
    (read and write) for a user to a specific category.
    '''

    user = get_user_or_raise_401(x_token)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin credentials are required for this option!")

    category_service.read_access(access)

    if access.can_write == 1:
        return f"User #{access.user_id} has writing and reading access to category #{access.category_id}"
    if access.can_write == 0 and access.can_read == 1:
        return f"User #{access.user_id} has reading access to category #{access.category_id}"

    return f"User #{access.user_id} has no read or write access rights to category #{access.category_id}"


@category_router.get('/privileged/{category_id}')
def privileged_users(category_id: int, x_token: str = Header()):
    '''
    Retrieve privileged users for a category.

    This endpoint allows an admin user to retrieve a list of privileged users 
    who have special access rights to a specific category.
    '''

    user = get_user_or_raise_401(x_token)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin credentials are required for this option!")

    return category_service.get_privileged(category_id)