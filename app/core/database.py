from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.core.config import Config

class Database:
    def __init__(self, uri) -> None:
        self.uri = uri
    
    def create(self) -> MongoClient:
        db = MongoClient(self.uri)

        print("Connected to MongoDB")

        return db["test"]