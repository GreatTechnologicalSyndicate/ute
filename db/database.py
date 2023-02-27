from pymongo import MongoClient
from config import database_name


class Database():
    def __init__(self, mongo_url: str):
        self.db = MongoClient(mongo_url)[database_name]
        self.users = self.db.users
        self.chats = self.db.chats
