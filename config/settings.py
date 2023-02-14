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
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
USE_NGROK = os.getenv('USE_NGROK', "False") == "True"
BASE_URL = os.getenv('BASE_URL')
PORT = int(os.getenv('PORT'))