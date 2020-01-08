import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='.flaskenv', verbose=False)

class Config:
    VK_APP_ID = os.getenv("VK_APP_ID")
    VK_SECRET_KEY = os.getenv("VK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False