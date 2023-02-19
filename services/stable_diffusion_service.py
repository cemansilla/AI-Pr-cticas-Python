import os
import hashlib
import datetime
from config.settings import *
import base64
import requests

class StableDiffusionService:
  def __init__(self):
    self.ckpt_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ckpt")

  def generate_image_name(self, prompt):
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")
    hash_obj = hashlib.sha256(date_str.encode())
    hash_str = hash_obj.hexdigest()

    prompt = prompt[:50]
    file_name = prompt.lower()
    file_name = ''.join(e for e in file_name if e.isalnum() or e.isspace())
    file_name = file_name.replace(' ', '_')
    file_name = ''.join([file_name, '--', hash_str, '.png'])

    return file_name

  def generate_from_prompt(self, prompt: str, ckpt: str):
    payload = {
      "prompt": prompt,
      #"steps": 20
    }
    
    # docs: https://github.com/AUTOMATIC1111/stable-diffusion-webui/discussions/3734
    override_settings = {}
    #override_settings["CLIP_stop_at_last_layers"] = 2

    ckpt_model = False
    if ckpt == 'inkpunk_diffusion':
      ckpt_model = "inkpunkDiffusion_v2.ckpt"
    elif ckpt == 'dreamshaper':
      ckpt_model = "dreamshaper_331BakedVae_ckpt.ckpt [fab0bb2f15]"
    elif ckpt == 'cedamansilla':
      ckpt_model = "cedamansilla.ckpt [36d52d87ff]"
    
    if ckpt_model != False:      
      override_settings["sd_model_checkpoint"] = ckpt_model
      override_payload = {
        "override_settings": override_settings
      }
      payload.update(override_payload)

    response = requests.post(STABLEDIFUSSION_API_BASE_URL + "txt2img", json=payload)

    file_name = self.generate_image_name(prompt)
    directory = 'data/images/api/stable-diffusion'
    output_path = os.path.join(directory, file_name)

    if not os.path.exists(directory):
      os.makedirs(directory)

    b64_image = response.json()['images'][0]    
    with open(output_path, "wb") as image_file:
      image_file.write(base64.b64decode(b64_image))

    return {
      "success": True,
      "image_path": output_path,
      "file_name": file_name
    }
  
  def get_models(self):
    response = requests.get(STABLEDIFUSSION_API_BASE_URL + "sd-models")

    return response.json()
