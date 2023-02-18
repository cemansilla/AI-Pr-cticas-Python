from typing import List
from werkzeug.utils import secure_filename
from services.openai_service import OpenAIService
from services.telegram_service import TelegramService

class TelegramController:
  def __init__(self):
    self.openai = OpenAIService()
    self.telegram = TelegramService()

  def send(self, request):
    if "message" in request:
      return self.telegram.send_message(request["message"])
    else:
      return {"error": "Petición incorrecta. Enviar parámetro message."}

  def updates(self, request):
    if "message" in request and "text" in request["message"]:
      prompt = request["message"]["text"]
    elif "message" in request and "voice" in request["message"]:
      response = self.telegram.get_file(request)

      if response['success']:
        transcribe_response = self.openai.transcribe(response['data']['path'])

        if "text" in transcribe_response:
          prompt = transcribe_response['text']
        else:
          prompt = "Generar mensaje gracioso para notificar que ocurrió un error procesando el mensaje de audio. Dar respuesta como si fuera un robot."
      else:
        prompt = "Generar mensaje gracioso para notificar que ocurrió un error entendiendo el mensaje de audio."
    else:
      prompt = "Generar mensaje gracioso para notificar que no entiendo el mensaje que me dijeron o que no tengo respuesta. Darme la respuesta directa, sin ninguna introducción ni cierre agregado a lo que pido. Tampoco entregar la respuesta entre comillas."

    gpt_response_text = self.openai.completion(prompt)

    self.telegram.send_message(gpt_response_text)
    return {"success": True}

  def set_webhook(self, request):    
    if "webhook_url" in request:
      return self.telegram.set_webhook(request["webhook_url"])
    else:
      return {"error": "Petición incorrecta. Enviar webhook_url."}

  def delete_webhook(self):
    #data = request.json()

    return self.telegram.delete_webhook()