from dotenv import dotenv_values
import os

current_dir = os.path.dirname(__file__)

env_path = os.path.join(current_dir, '../../.env')

env_values = dotenv_values(env_path)

class Config:
    PROJECT_NAME = "Cefalo Python Assignment"
    MONGODB_URI = env_values.get('MONGODB_URI')
    API = "/api"
    API_V1_STR = "/api/v1"