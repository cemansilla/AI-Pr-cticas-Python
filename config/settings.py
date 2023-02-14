import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

DATABASE_URI = os.getenv('DATABASE_URI')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')