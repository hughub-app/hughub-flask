# config.py
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from a .env file if present

class Config:
    API_TITLE = "Child Emotional Health API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  # PostgreSQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
