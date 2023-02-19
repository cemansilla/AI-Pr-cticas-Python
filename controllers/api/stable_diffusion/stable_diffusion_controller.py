import requests
from fastapi import HTTPException
from services.stable_diffusion_service import StableDiffusionService
from config.settings import *

class StableDiffusionController:
  def __init__(self):
    self.sd = StableDiffusionService()

  def generate_from_prompt(self, request):    
    result = None

    if 'prompt' in request and 'ckpt' in request:
      try:
        result = self.sd.generate_from_prompt(request['prompt'], request['ckpt'])
      except Exception as e:
        result = {'success': False, 'error_code': 'ERROR_DOWNLOAD', 'error_message': str(e)}
    else:
      raise HTTPException(status_code=400, detail="Petición incorrecta. Enviar parámetro prompt y ckpt.")

    return result
  
  def get_models(self):
    return self.sd.get_models()