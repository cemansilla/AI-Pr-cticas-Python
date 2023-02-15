from fastapi import Request
from typing import List
import os
from werkzeug.utils import secure_filename
from services.openai_service import OpenAIService
from services.telegram_service import TelegramService

class TelegramController:
  def __init__(self):
    self.openai = OpenAIService()
    self.telegram = TelegramService()

  async def send(self, request: Request):
    message = await request.json()
    if "message" in message:
      return await self.telegram.send_message(message["message"])
    else:
      return {"error": "Petición incorrecta. Enviar parámetro message."}

  async def updates(self, request: Request):
    data = await request.json()
    if "message" in data and "text" in data["message"]:
      prompt = data["message"]["text"]
    elif "message" in data and "voice" in data["message"]:
      response = await self.telegram.get_file(data)

      print("En TelegramController. Tengo la respuesta de la descarga del archivo de audio", response)
      print("Debería llamar a self.openai.transcribe")
      #self.openai.transcribe(response.path)

      prompt = "Generar mensaje gracioso para notificar que esta funcionalidad aún está en desarrollo. Darme la respuesta directa, sin ninguna introducción ni cierre agregado a lo que pido. Tampoco entregar la respuesta entre comillas."
    else:
      prompt = "Generar mensaje gracioso para notificar que no entiendo el mensaje que me dijeron o que no tengo respuesta. Darme la respuesta directa, sin ninguna introducción ni cierre agregado a lo que pido. Tampoco entregar la respuesta entre comillas."

    gpt_response_text = self.openai.completion(prompt)

    await self.telegram.send_message(gpt_response_text)
    return {"success": True}

  def whisper_handle(self, response):
    return response

  async def set_webhook(self, request: Request):
    data = await request.json()
    if "webhook_url" in data:
      return await self.telegram.set_webhook(data["webhook_url"])
    else:
      return {"error": "Petición incorrecta. Enviar webhook_url."}

  async def do_upload_file(self, file):
    print("do_upload_file temporal")
    #return {"hello":"world"}
    
    directory = '/content/uploads/'
    if not os.path.exists(directory):
      os.makedirs(directory)

    filename = secure_filename(file.filename)

    with open(os.path.join(directory, filename), 'wb') as f:
      f.write(await file.read())

    reeponse = {'directory': directory, 'filename': filename, 'success': True}
    return await self.whisper_handle(reeponse)   
