from dotenv import dotenv_values
import os

current_dir = os.path.dirname(__file__)

env_path = os.path.join(current_dir, '../../.env')

env_values = dotenv_values(env_path)

class Config:
    MONGO_URI = env_values.get('MONGO_URI')