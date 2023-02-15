from typing import List
import os
import logging
from werkzeug.utils import secure_filename
from services.openai_service import OpenAIService
from services.telegram_service import TelegramService

class TelegramController:
  def __init__(self):
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    logging.basicConfig(filename=os.path.join(log_directory, 'telegram_controller.log'), encoding='utf-8', level=logging.DEBUG)

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
      logging.debug("recibí mensaje de texto")
      logging.info(request)
    elif "message" in request and "voice" in request["message"]:
      logging.debug("recibí mensaje de audio")
      logging.info(request)
      response = self.telegram.get_file(request)

      logging.debug("response de get_file")
      logging.info(response)
      if response['success']:
        print("if success")
        transcribe_response = self.openai.transcribe(response['data']['path'])
        print('transcribe_response', transcribe_response)
      else:
        print("else success")

      prompt = "Generar mensaje gracioso para notificar que esta funcionalidad aún está en desarrollo. Darme la respuesta directa, sin ninguna introducción ni cierre agregado a lo que pido. Tampoco entregar la respuesta entre comillas."
    else:
      logging.debug("recibí mensaje sin detectar tipo, sale por defecto")
      prompt = "Generar mensaje gracioso para notificar que no entiendo el mensaje que me dijeron o que no tengo respuesta. Darme la respuesta directa, sin ninguna introducción ni cierre agregado a lo que pido. Tampoco entregar la respuesta entre comillas."

    gpt_response_text = self.openai.completition(prompt)

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