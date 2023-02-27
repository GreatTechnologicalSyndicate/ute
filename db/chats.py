

class Chats:
    def __init__(self, db):
        self.db = db.chats
        self.database = db
        self.initialize()

    def initialize(self):
        sample = self.db.find_one({})
        for line, value in self.form_chat_doc(0, "0").items():
            if line not in sample:
                self.db.update_many({}, {"$set": {line: value}})

    def get_chats(self):
        return self.db.find({})

    @property
    def chats(self):
        return [chat['_id'] for chat in self.db.find({})]

    def ban(self, chat_id, user_id):
        self.db.update_one({'_id': chat_id}, {'$addToSet': {'banned': user_id}})

    def unban(self, chat_id, user_id):
        self.db.update_one({'_id': chat_id}, {'$pull': {'banned': user_id}})

    def delete_chat(self, chat_id):
        self.db.delete_one({'_id': chat_id})

    def create_chat(self, chat_id: int, title: str):
        chat = self.form_chat_doc(chat_id, title)
        if self.get_chat(chat_id):
            return
        self.db.insert_one(chat)
        return chat
    
    def get_chat(self, chat_id: int):
        return self.db.find_one({'_id': chat_id})

    def form_chat_doc(self, chat_id: int, title: str):
        return {
            '_id': chat_id,
            'title': title,
            'banned': [],
            'administrators': []
        }