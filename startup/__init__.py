from config import *
from telebot import TeleBot

from db import Database


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

self_id = bot.get_me().id
