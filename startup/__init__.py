from aiogram import Bot, Dispatcher
from telebot import TeleBot

from config import *
from db import Database


class ExtendedBot(Bot):
    def form_html_mlink(self, m, text):
        chat_id = int(str(m.chat.id).split('-100', 1)[1])
        return f'[{text}](https://t.me/c/{chat_id}/{m.message_id})'


bot = ExtendedBot(telegram_token)
tbot = TeleBot(telegram_token)
dp = Dispatcher(bot)
dp.message_handlers.once = False
db = Database(mongo_url)
