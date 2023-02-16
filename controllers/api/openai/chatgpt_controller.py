import logging
from fastapi import HTTPException
from services.openai_service import OpenAIService

class ChatGPTController:
  def __init__(self):
    self.openai = OpenAIService()

  def chat(self, request):    
    result = None

    if 'prompt' in request:
      result = self.openai.completion(request['prompt'])
    else:
      raise HTTPException(status_code=400, detail="Petición incorrecta. Enviar parámetro prompt.")

    return result