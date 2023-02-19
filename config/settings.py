import os
import sys
from dotenv import load_dotenv,find_dotenv

IN_COLAB = 'google.colab' in sys.modules

if IN_COLAB:
  with open(".env.example") as source_file:
    source_data = source_file.read()

  with open(".env", "w") as target_file:
    target_file.write(source_data)

load_dotenv(find_dotenv())

DATABASE_URI = os.getenv('DATABASE_URI')
USE_NGROK = os.getenv('USE_NGROK', "False") == "True"
BASE_URL = os.getenv('BASE_URL')
PORT = int(os.getenv('PORT'))
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_BASE_URL=os.getenv('OPENAI_API_BASE_URL')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_GROUP_ID = os.getenv('TELEGRAM_GROUP_ID')
TELEGRAM_PERSONAL_ID = os.getenv('TELEGRAM_PERSONAL_ID')
TELEGRAM_API_BASE_URL=os.getenv('TELEGRAM_API_BASE_URL')
STABLEDIFUSSION_API_BASE_URL=os.getenv('STABLEDIFUSSION_API_BASE_URL')
PYTHON_API_URL=os.getenv('PYTHON_API_URL')