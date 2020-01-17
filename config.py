import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='.flaskenv', verbose=False)

class Config:
    VK_APP_ID = os.getenv("VK_APP_ID")
    VK_SECRET_KEY = os.getenv("VK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
#    SESSION_TYPE = os.getenv("SESSION_TYPE")
#    SESSION_SQLALCHEMY = os.getenv("SESSION_SQLALCHEMY")
#    SESSION_SQLALCHEMY_TABLE = os.getenv("SESSION_SQLALCHEMY_TABLE")
#    SESSION_PERMANENT = bool(os.getenv("SESSION_PERMANENT"))
#    PERMANENT_SESSION_LIFETIME = int(os.getenv("PERMANENT_SESSION_LIFETIME"))
