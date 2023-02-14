from typing import List
from config.settings import *

def get_home():
  return {
    "Hola": "Mundo!!"
  }

def get_items(item_id: int):
  # Aquí va la lógica para obtener un ítem específico
  item = {"id": item_id, "name": "Item {}".format(item_id)}
  return item

def get_all_items():
  # Aquí va la lógica para obtener todos los ítems
  items = [{"id": i, "name": "Item {}".format(i)} for i in range(1, 11)]
  return items

def get_variable_entorno():
  return {
    'DATABASE_URI': DATABASE_URI,
    'JWT_SECRET_KEY': JWT_SECRET_KEY
  }