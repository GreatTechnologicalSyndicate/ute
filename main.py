from bot import *
from startup import dp, bot
from aiogram import executor
from asyncio import new_event_loop


async def boot():
    await bot.send_message(log_channel, '♻️✅')
new_event_loop().run_until_complete(boot())
executor.start_polling(dp, skip_updates=True)
