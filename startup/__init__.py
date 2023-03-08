#  Universal Telegram Ecosystem - bot for chat management
#  Copyright (C) 2023  Great Technological Syndicate
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

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
