from config import *
from telebot import TeleBot
from db.database import Database
from db.chats import Chats
from db.users import Users

class ExtendedBot(TeleBot):
    def form_html_userlink(self, name, user_id):
        return f'<a href="tg://user?id={user_id}">{name}</a>'

    def form_html_messagelink(self, m, text):
        chat_id = int(str(m.chat.id).split('-100', 1)[1])
        return f'[{text}](https://t.me/c/{chat_id}/{m.message_id})'

    def respond_to(self, message, text, **kwargs):
        return self.send_message(message.chat.id, text, **kwargs)

bot = ExtendedBot(telegram_token)
db = Database(mongo_url)
users = Users(db)
chats = Chats(db)

self_id = bot.get_me().id

for owner in owners:
    users.db.update_one({'_id': owner}, {'$set': {'status': 'owner'}})
