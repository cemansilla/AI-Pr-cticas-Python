import logging
import os
from fastapi import HTTPException
from services.openai_service import OpenAIService

class ChatGPTController:
  def __init__(self):
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    logging.basicConfig(filename=os.path.join(log_directory, 'chatgpt_controller.log'), encoding='utf-8', level=logging.DEBUG)

  def chat(request):
    openai = OpenAIService()
    result = None

    if 'prompt' in request:
      result = openai.completion(request['prompt'])
    else:
      raise HTTPException(status_code=400, detail="Petición incorrecta. Enviar parámetro prompt.")

    return result