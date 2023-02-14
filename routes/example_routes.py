from fastapi import APIRouter
from .example_controller import get_item

router = APIRouter()

@router.get("/items/{item_id}")
def read_item(item_id: int):
  return get_items(item_id)

@router.get("/items/")
def read_item():
  return get_all_items()