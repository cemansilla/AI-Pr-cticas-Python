from typing import List
import os
import logging
from werkzeug.utils import secure_filename
from services.openai_service import OpenAIService
from services.telegram_service import TelegramService

class TelegramController:
  def __init__(self):
    self.openai = OpenAIService()
    self.telegram = TelegramService()
    logging.basicConfig(filename='telegram_controller.log', level=logging.DEBUG)

  def send(self, request):
    if "message" in request:
      return self.telegram.send_message(request["message"])
    else:
      return {"error": "Petición incorrecta. Enviar parámetro message."}

  def updates(self, request):
    if "message" in request and "text" in request["message"]:
      prompt = request["message"]["text"]
      logging.info("recibí mensaje de texto", extra={'prompt':prompt})
    elif "message" in request and "voice" in request["message"]:
      logging.info("recibí mensaje de audio", extra={'request':request})
      response = self.telegram.get_file(request)

      print("En TelegramController. Tengo la respuesta de la descarga del archivo de audio", response)
      print("Debería llamar a self.openai.transcribe")
      #self.openai.transcribe(response.path)

      prompt = "Generar mensaje gracioso para notificar que esta funcionalidad aún está en desarrollo. Darme la respuesta directa, sin ninguna introducción ni cierre agregado a lo que pido. Tampoco entregar la respuesta entre comillas."
    else:
      logging.info("recibí mensaje sin detectar tipo, sale por defecto")
      prompt = "Generar mensaje gracioso para notificar que no entiendo el mensaje que me dijeron o que no tengo respuesta. Darme la respuesta directa, sin ninguna introducción ni cierre agregado a lo que pido. Tampoco entregar la respuesta entre comillas."

    gpt_response_text = self.openai.completition(prompt)

    self.telegram.send_message(gpt_response_text)
    return {"success": True}

  def whisper_handle(self, response):
    return response

  def set_webhook(self, request):    
    if "webhook_url" in request:
      return self.telegram.set_webhook(request["webhook_url"])
    else:
      return {"error": "Petición incorrecta. Enviar webhook_url."}

  def delete_webhook(self):
    #data = request.json()

    return self.telegram.delete_webhook()

  def do_upload_file(self, file):
    print("do_upload_file temporal")
    #return {"hello":"world"}
    
    directory = '/content/uploads/'
    if not os.path.exists(directory):
      os.makedirs(directory)

    filename = secure_filename(file.filename)

    with open(os.path.join(directory, filename), 'wb') as f:
      f.write(file.read())

    reeponse = {'directory': directory, 'filename': filename, 'success': True}
    return self.whisper_handle(reeponse)   
