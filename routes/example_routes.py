from fastapi import APIRouter
from controllers.example_controller import *

router = APIRouter()

@router.get("/")
async def home():
  return get_home()

@router.get("/items/{item_id}")
async def read_item(item_id: int):
  return get_items(item_id)

@router.get("/items")
async def read_item():
  return get_all_items()

@router.get("/test")
async def variable_entorno():
  return get_variable_entorno()