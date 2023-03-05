from config import *
from db import status
from startup import db, bot, tbot


def command(text=None, req_status=status.GUEST, reply=False, arguments=False, self_admin_rights=False):
    def decorator(func):
        wrapper = for_status(req_status)(func)
        if text:
            wrapper = for_text(text)(wrapper)
        if reply:
            wrapper = reply_lambda(wrapper)
        if arguments:
            wrapper = arguments_lambda(wrapper)
        if self_admin_rights:
            wrapper = self_admin_check(wrapper)
        return wrapper
    return decorator


def for_text(text):
    def decorator(func):
        async def wrapper(m):
            if m.text.lower() == text or m.text == text:
                await func(m)

        return wrapper

    return decorator


def for_status(value):
    def decorator(func):
        async def wrapper(m):
            user = db.process_tg_user(m.from_user)
            if user.is_status(value):
                await func(m)

        return wrapper

    return decorator


def check_ban(func):
    async def wrapper(m):
        user = db.process_tg_user(m.from_user)
        if user:
            return lambda _: _
        await func(m)

    return wrapper


def arguments_lambda(func):
    async def wrapper(m):
        if m.text.count(' '):
            await func(m)

    return wrapper


def reply_lambda(func):
    async def wrapper(m):
        if m.reply_to_message:
            await func(m)

    return wrapper


def shana_lamda(m):
    return m.text.lower() in shana_commands


def ganyba_lamda(m):
    return m.text.lower() in ganyba_commands


def owner_callback(c):
    return c.from_user.id in db.owners


def join_request_callback(c):
    return c.data.startswith('ja ') or c.data.startswith('jd ')


def butterfly(m):
    return m.text == allow_chat_command


def self_admin_check(func):
    async def wrapper(m):
        if tbot.get_chat_member(m.chat.id, bot.id).status == 'admin':
            await func(m)
        else:
            return lambda _: tbot.send_message(log_channel, f'🔨❔ | {m.chat.title} | {m.chat.id}')

    return wrapper


def chat_admin_check(m):
    user = db.process_tg_user(m.from_user)
    tg_user = tbot.get_chat_member(m.chat.id, m.from_user.id)
    if user.owner:
        return True
    if tg_user.status == 'admin':
        return True
    if tg_user.status == 'creator':
        return True
    return False


def chat_check_lambda(m):
    if m.chat.type == 'private':
        return False
    if butterfly(m) and db.process_tg_user(m.from_user).owner:
        tbot.send_message(log_channel,
                          f'{allow_chat_command}✅`{m.chat.id}`|{m.chat.title}\n\n{bot.form_html_mlink(m, "🔍🔍🔍")}',
                          parse_mode='Markdown')
        db.create_chat(m.chat.id, m.chat.title)
    if m.chat.id not in db.chats:
        if m.new_chat_members:
            if m.new_chat_members[0].id == bot.id:
                return False
        return True
