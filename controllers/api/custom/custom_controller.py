import requests
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