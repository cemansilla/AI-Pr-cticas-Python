import os
import hashlib
import datetime
import pyttsx3
from fastapi import HTTPException
from config.settings import *

class TextToSpeechController:
  def __init__(self):
    pass

  def text_to_speech(self, request):    
    result = None

    if 'text' in request:
      try:
        texto = request['text']

        file_name = self.generate_file_name(texto, 'wav')
        directory = 'data/audios/text-to-speech'
        audio_path = os.path.join(directory, file_name)

        if not os.path.exists(directory):
          os.makedirs(directory)

        engine = pyttsx3.init()

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)

        # Salida hablada del audio
        #engine.say(texto)

        # Almacenamiento del audio en archivo
        engine.save_to_file(texto, audio_path)

        engine.runAndWait()

        result = {
          "success": True,
          "text": texto,
          "file_name": file_name
        }
      except Exception as e:
        result = {'success': False, 'error_code': 'ERROR_TTS', 'error_message': str(e)}
    else:
      raise HTTPException(status_code=400, detail="Petición incorrecta. Enviar parámetro text.")

    return result
  
  def generate_file_name(self, text, extension):
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")
    hash_obj = hashlib.sha256(date_str.encode())
    hash_str = hash_obj.hexdigest()

    text = text[:50]
    file_name = text.lower()
    file_name = ''.join(e for e in file_name if e.isalnum() or e.isspace())
    file_name = file_name.replace(' ', '_')
    file_name = ''.join([file_name, '--', hash_str, '.', extension])

    return file_name