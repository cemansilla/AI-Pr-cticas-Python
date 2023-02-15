from fastapi import Request,HTTPException
from services.openai_service import OpenAIService

class ChatGPTController:
  async def chat(request: Request):
    openai = OpenAIService()
    prompt = await request.json()
    result = None

    if 'prompt' in prompt:
      result = openai.completion(prompt['prompt'])
    else:
      raise HTTPException(status_code=400, detail="Petición incorrecta. Enviar parámetro prompt.")

    return result