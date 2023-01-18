from pymongo import MongoClient
from config import mongo_url


class Database():
    def __init__(self, mongo_url: str):
        self.db = MongoClient(mongo_url).imf
        self.users = self.db.users
        self.chats = self.db.chats
