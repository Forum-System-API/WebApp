from fastapi import APIRouter, Response, status, HTTPException
from data.models import Category
from services import category_service


category_router = APIRouter(prefix='/category')

@category_router.get("/")
def show_categories():
    categories = category_service.all()

@category_router.get("/{category_name}")
def show_category_by_name(category_name:str):
    category = category_service.find_by_name(category_name)