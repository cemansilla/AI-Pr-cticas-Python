import requests
import pytesseract
import nltk
from PIL import Image
import os
from fastapi import HTTPException
from services.openai_service import OpenAIService
from services.stable_diffusion_service import StableDiffusionService
from config.settings import *

class CustomController:
  def __init__(self):
    self.specs = {
      "instagram": {
        "image": {      
          "width": 1080,"height": 1080
        },
        "text": {
          "max_length": 2200,
          "optimal_lenght": 140
        }
      },
      "facebook": {
        "image": {      
          "width": 1200,"height": 630
        },
        "text": {
          "max_length": 90,
          "optimal_lenght": 70
        }
      },
      "twitter": {
        "image": {      
          "width": 1600,"height": 900
        },
        "text": {
          "max_length": 140,
          "optimal_lenght": 100
        }
      },
      "linkedin": {
        "image": {      
          "width": 1200,"height": 627
        },
        "text": {
          "max_length": 3000,
          "optimal_lenght": 2500
        }
      },
      "default": {
        "image": {      
          "width": 1024,"height": 1024
        },
        "text": {
          "max_length": 250,
          "optimal_lenght": 200
        }
      }
    }

    self.openai = OpenAIService()
    self.sd = StableDiffusionService()

  def sentiment(self, request):    
    result = None

    if 'text' in request:
      try:
        nltk.download('vader_lexicon')
        from nltk.sentiment.vader import SentimentIntensityAnalyzer

        texto_spanish = request['text']
        texto_english = self.openai.completion(f"Traducir a inglés el siguiente texto, no agregar ninguna introducción ni cierre a la frase, solo devolver la traducción: {texto_spanish}")
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(texto_english)

        analysis_result = f"El texto \"{texto_spanish}\" ha sido catalogado como: "
        if scores['compound'] >= 0.05 :
          analysis_result += "positivo"
        elif scores['compound'] <= - 0.05 :
          analysis_result += "negativo"
        else :
          analysis_result += "neutral"

        result = {
          "success": True,
          "scores": scores,
          "diagnosis": analysis_result
        }
      except Exception as e:
        result = {'success': False, 'error_code': 'ERROR_NLTK', 'error_message': str(e)}
    else:
      raise HTTPException(status_code=400, detail="Petición incorrecta. Enviar parámetro text.")

    return result

  """
  TODO: En construcción...
  """
  def ocr(self, file_contents: bytes, file_name: str):
    pytesseract.pytesseract.tesseract_cmd = 'D:/Tesseract-OCR/tesseract.exe'

    directory = 'data/images/ocr'
    path = os.path.join(directory, file_name)

    if not os.path.exists(directory):
      os.makedirs(directory)

    with open(path, 'wb') as f:
      f.write(file_contents)

    image = Image.open(path)
    to_string = pytesseract.image_to_string(image)
    to_osd = pytesseract.image_to_osd(image)
    to_data = pytesseract.image_to_data(image)

    # Procesar el texto
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    tokens = nltk.word_tokenize(to_string)
    tags = nltk.pos_tag(tokens)

    productos = self.parse_tags(tags)    

    """
    "file_name": file_name,
    "to_string": to_string,
    "to_data": to_data,
    "to_osd": to_osd,
    "tokens": tokens,
    """
    return {
      "success": True,
      "productos": productos,
    }

  """
  TODO: Funcionalidad a desarrollar
        Depende de la estructura de cada ticket
        Debería retornar la data y en caso de no poder hacerlo debería almacenar en base de datos
        alguna marca que indique que hay que reprocesar el ticket
  """
  def parse_tags(self, tags):
    productos = [
      {"item":"Fake name","price":123.34},
      {"item":"Fake name 1","price":231.46},
      {"item":"Fake name 2","price":332.97},
    ]
    """
    productos = []
    for i, (item, pos) in enumerate(tags):
      print(i, item, pos)
    """

    return productos

  def generate_post_rrss(self, request):    
    result = None

    if 'prompt' in request and 'destino' in request:
      sizes = self.get_sizes_specs_by_rrss(request['destino'])
      
      prompt_text = f"Elaborar un posteo con el siguiente objetivo: {request['prompt']}"
      if request['destino']:
        prompt_text += f". Debe ser para la red social {request['destino']}"
      prompt_text += f". Debe tener idealmente {sizes['text']['optimal_lenght']} caracteres y como máximo {sizes['text']['max_length']} caracteres."
      result_text = self.openai.completion(prompt_text)

      prompt_image_text = f"Generar prompt para solicitar una imagen a Dall-E con el siguiente obtetivo: {request['prompt']}. No hacer introducción ni cierre en el texto generado, solo reponder con el prompt solicitado. Debe estar en inglés."
      prompt_image = self.openai.completion(prompt_image_text)
      result_image = self.sd.generate_from_prompt(prompt_image, "default", sizes['image']['width'], sizes['image']['height'])

      result = {'success': True, 
                'results': {
                  'text': result_text,
                  'image': result_image['file_name']
                }
              }
    else:
      raise HTTPException(status_code=400, detail="Petición incorrecta. Enviar parámetro y destino.")

    return result
  
  def get_sizes_specs_by_rrss(self, rrss: str):
    if rrss in self.specs:
      return self.specs[rrss]
    else:
      return self.specs['default']