import logging
from fastapi import HTTPException
from services.openai_service import OpenAIService

class ChatGPTController:
  def __init__():
    logging.basicConfig(filename='chatgpt_controller.log', level=logging.DEBUG)

  def chat(request):
    openai = OpenAIService()
    result = None

    if 'prompt' in request:
      result = openai.completion(request['prompt'])
    else:
      raise HTTPException(status_code=400, detail="Petición incorrecta. Enviar parámetro prompt.")

    return result