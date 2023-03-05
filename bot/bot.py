import time
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from .lambdas import *
from db import status
from startup import dp, bot
from aiogram.types import ContentType


@dp.message_handler(chat_check_lambda)
async def chat_check_handler(m):
    try:
        await bot.leave_chat(m.chat.id)
    except:
        return
    await bot.send_message(log_channel,
                           f'{allow_chat_command}❌`{m.chat.id}`|{m.chat.title}\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                           parse_mode='Markdown')


@dp.message_handler(user_check_lambda, content_types=ContentType.ANY)
async def user_check_handler(m):
    pass


@dp.chat_join_request_handler()
async def chat_join_request(r):
    kb = InlineKeyboardMarkup()
    user = db.process_tg_user(r.from_user)
    info = f'\n🗺💬: {r.chat.title}\n' + f'👤: {user.link()}'
    if user.banned:
        tts = '📬🔨❌' + info
        await bot.decline_chat_join_request(r.chat.id, user.id)
        await bot.send_message(log_channel, tts, parse_mode='HTML', reply_markup=kb)
        return
    elif user.owner:
        tts = f'📬{user.emoji}✅' + info
        await bot.approve_chat_join_request(r.chat.id, user.id)
        await bot.send_message(log_channel, tts, parse_mode='HTML', reply_markup=kb)
        return

    tts = '📬💬!' + info

    kb.add(InlineKeyboardButton('✅', callback_data=f'ja {r.chat.id} {r.from_user.id}'))
    kb.add(InlineKeyboardButton('❌', callback_data=f'jd {r.chat.id} {r.from_user.id}'))

    await bot.send_message(log_channel, tts, parse_mode='HTML', reply_markup=kb)


@dp.callback_query_handler(join_request_callback)
async def jc_handler(c):
    accept = True if c.data[1] == 'a' else False
    chat_id = int(c.data.split()[1])
    user_id = int(c.data.split()[2])
    m = c.message
    tts = m.text
    if accept:
        await bot.approve_chat_join_request(chat_id, user_id)
        await bot.edit_message_text(f'{tts}\n✅Принято!', m.chat.id, m.message_id, parse_mode='HTML')
    else:
        await bot.decline_chat_join_request(chat_id, user_id)
        await bot.edit_message_text(f'{tts}\n❌Отклонено!', m.chat.id, m.message_id, parse_mode='HTML')


@dp.message_handler()
@for_text(global_unban_command)
@for_status(status.OWNER)
@reply_lambda
async def unban_handler(m):
    user = db.process_tg_user(m.reply_to_message.from_user)
    await m.answer(f'{m.text}✅')
    db.unban_user(user.id)
    for chat_id in db.chats:
        try:
            await bot.unban_chat_member(chat_id, user.id)
        except:
            chat = db.get_chat(chat_id)
            await bot.send_message(log_channel, f'🔨❔ | {chat.title} | {chat.id}')
    await bot.send_message(log_channel, f'{m.text}✅ | `{user.id}`\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                           parse_mode='Markdown')


@dp.message_handler()
@for_text(global_ban_command)
@for_status(status.OWNER)
@reply_lambda
async def ban_handler(m):
    user = db.process_tg_user(m.reply_to_message.from_user)
    await m.answer(f'{m.text}✅')
    db.ban_user(user.id)
    for chat_id in db.chats:
        try:
            await bot.ban_chat_member(chat_id, user.id)
        except:
            chat = db.get_chat(chat_id)
            await bot.send_message(log_channel, f'🔨❔ | {chat.title} | {chat.id}')
    await bot.send_message(log_channel, f'{m.text}✅ | `{user.id}`\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                           parse_mode='Markdown')


@dp.message_handler()
@for_text(promote_command)
@for_status(status.OWNER)
@reply_lambda
async def promote_handler(m):
    user = db.process_tg_user(m.reply_to_message.from_user)
    user.set_status(status.OWNER)
    await bot.send_message(log_channel,
                           f'{m.text}✅ | `{user.id}` | `{m.chat.id}`\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                           parse_mode='Markdown')


@dp.message_handler()
@for_text(grant_membership_command)
@for_status(status.OWNER)
async def member_handler(m):
    user = db.process_tg_user(m.reply_to_message.from_user)
    user.set_status(status.MEMBER)
    await bot.send_message(log_channel,
                           f'{m.text}✅ | `{user.id}` | `{m.chat.id}`\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                           parse_mode='Markdown')


@dp.message_handler(lambda m: shana_lamda(m) or ganyba_lamda(m))
@for_status(status.MEMBER)
async def reputation_handler(m):
    if m.from_user.id == m.reply_to_message.from_user.id or m.reply_to_message.from_user.is_bot:
        await m.answer('Choose a human please (not yourself)')
        return
    communicator = db.process_tg_user(m.from_user)
    time_now = time.time()
    cooldown_time = 3 * 60 * 60
    time_differ = time_now - communicator.reputation_cooldown
    if time_differ < cooldown_time:
        hours, remainder = divmod(cooldown_time - time_differ, 3600)  # 3600 seconds in an hour
        minutes, seconds = divmod(remainder, 60)  # 60 seconds in a minute
        await m.answer(f"Wait for {int(hours)}:{int(minutes)}:{int(seconds)}")
        return

    user = db.process_tg_user(m.reply_to_message.from_user)
    user.reputation += 1 if shana_lamda(m) else -1
    communicator.reputation_cooldown = time_now
    user.save()
    communicator.save()

    await m.answer(f'🆙 {user.name} {"+1" if shana_lamda(m) else "-1"} rep')


@dp.message_handler(commands=['achievement'])
@for_status(status.OWNER)
@arguments_lambda
@reply_lambda
async def achievement_handler(m):
    award = m.text.split(' ', 1)[1]
    user = db.process_tg_user(m.reply_to_message.from_user)
    user.add_award(award)
    await m.reply('🏆✅')


@dp.message_handler(commands=['global_ban'])
@for_status(status.OWNER)
@arguments_lambda
async def global_ban_handler(m):
    user = db.get_user(int(m.text.split(' ', 1)[1]))
    user.ban()
    await m.answer(f'{m.text}✅')
    for chat in db.get_chats():
        try:
            await bot.ban_chat_member(chat.id, user.id)
        except:
            await bot.send_message(log_channel, f'🔨❔ | {chat.title} | {chat.id}')
    await bot.send_message(log_channel, f'{m.text}✅ | `{user.id}`\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                           parse_mode='Markdown')


@dp.message_handler(commands=['map'])
@for_status(status.OWNER)
async def map_handler(m):
    tts = '🗺📃:\n'
    for chat in db.get_chats():
        try:
            link = await bot.export_chat_invite_link(chat.id)
        except:
            link = '0.0.0.0/error'
        tts += f'<a href="{link}">{chat.title}</a> - {chat.id}\n'
    await m.answer(tts, parse_mode='HTML')


@dp.message_handler(commands=['banlist'])
@for_status(status.OWNER)
async def map_handler(m):
    tts = '🔨📃:\n'
    for user in db.User.objects(status=status.BANNED):
        tts += f'{user.link()}\n'
    await m.answer(tts, parse_mode='HTML')


@dp.message_handler(commands=['rep'])
@for_status(status.MEMBER)
async def rep_handler(m):
    tts = '🔂📃:\n'
    for user, position in db.get_top_reputation():
        tts += f'{position}.{user.emoji}{user.name} - {user.reputation}\n'
    await m.answer(tts, parse_mode='HTML')


@dp.message_handler(commands=[status.MEMBER + 's'])
@for_status(status.OWNER)
async def members_handler(m):
    tts = '🛂📃:\n'
    for user in db.User.objects(status=status.MEMBER):
        tts += f'{user.link()}\n'
    await m.answer(tts, parse_mode='HTML')


@dp.message_handler(commands=['profile'])
async def profile_handler(m):
    user = m.from_user
    if m.reply_to_message:
        user = m.reply_to_message.from_user
    user = db.process_tg_user(user)
    await m.answer(user.profile())


@dp.message_handler(commands=['owners'])
@for_status(status.OWNER)
async def owners_handler(m):
    print('Working here!')
    tts = ''
    for owner in db.get_owners():
        tts += f"{owner.link()}`\n"
    await m.answer(tts, parse_mode="Markdown")


@dp.message_handler(commands=['start'])
async def start_handler(m):
    await m.answer('👋')
