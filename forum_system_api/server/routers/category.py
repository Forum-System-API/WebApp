from fastapi import APIRouter, Response, status, HTTPException
from data.models import Category
from services import category_service


category_router = APIRouter(prefix='/category')

@category_router.get("/")
def show_categories():
    pass