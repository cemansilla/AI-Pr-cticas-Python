from typing import List

def get_items(item_id: int):
  # Aquí va la lógica para obtener un ítem específico
  item = {"id": item_id, "name": "Item {}".format(item_id)}
  return item

def get_all_items():
  # Aquí va la lógica para obtener todos los ítems
  items = [{"id": i, "name": "Item {}".format(i)} for i in range(1, 11)]
  return items