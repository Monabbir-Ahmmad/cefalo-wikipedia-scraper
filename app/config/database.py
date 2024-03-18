from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.config.settings import Config

client = MongoClient(Config.MONGO_URI, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['test']
