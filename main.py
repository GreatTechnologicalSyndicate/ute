from aiogram import executor

from bot import *
from startup import dp, tbot

tbot.send_message(log_channel, '♻️✅')
executor.start_polling(dp, skip_updates=True)
