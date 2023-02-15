import os
import json
import requests
from fastapi import HTTPException
from services.openai_service import OpenAIService
from config.settings import *

class TelegramService:
  def __init__(self, openai_service: OpenAIService):
    self.openai_service = openai_service

  def send_message(self, message: str) -> dict:
    api_url = TELEGRAM_API_BASE_URL + "bot" + TELEGRAM_BOT_TOKEN + "/sendMessage"

    response = requests.post(api_url, data={
      "chat_id": TELEGRAM_PERSONAL_ID,
      "text": message
    })

    if not response.ok:
      raise HTTPException(status_code=500, detail="Error sending Telegram message")

    return json.loads(response.text)

  def set_webhook(self, webhook_url: str) -> dict:
    api_url = TELEGRAM_API_BASE_URL + "bot" + TELEGRAM_BOT_TOKEN + "/setWebhook?url=" + webhook_url

    response = requests.get(api_url)

    if not response.ok:
      raise HTTPException(status_code=500, detail="Error setting Telegram webhook")

    return json.loads(response.text)

  def get_file(self, data: dict) -> dict:
    response = {'success': False, 'error_code': 'UNKNOWN'}

    api_url = TELEGRAM_API_BASE_URL + "bot" + TELEGRAM_BOT_TOKEN + "/getFile"

    file_id = data['message']['voice']['file_id']
    file_unique_id = data['message']['voice']['file_unique_id']

    get_file_response = requests.get(api_url, params={
      'file_id': file_id
    })

    if get_file_response.ok:
      body = json.loads(get_file_response.text)
      file_path = body['result']['file_path']
      download_uri = TELEGRAM_API_BASE_URL + "file/bot" + TELEGRAM_BOT_TOKEN + "/" + file_path

      try:
        extension = os.path.splitext(file_path)[1]

        directory = 'audios'
        file = os.path.join(directory, file_unique_id + extension)
        path = os.path.join(directory, file)

        if not os.path.exists(directory):
          os.makedirs(directory)

        download_response = requests.get(download_uri)

        if download_response.ok:
          with open(path, 'wb') as f:
            f.write(download_response.content)

          response = {'success': True, 'data': {
            'filename': file,
            'path': path
          }}
        else:
          response = {'success': False, 'error_code': 'ERROR_DOWNLOAD'}
      except Exception as e:
        response = {'success': False, 'error_code': 'ERROR_DOWNLOAD', 'error_message': str(e)}
    else:
      response = {'success': False, 'error_code': 'ERROR_STATUS_CODE'}

    return response
