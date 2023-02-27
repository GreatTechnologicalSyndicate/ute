from .startup import bot, users, chats, self_id
from config import *


def check_ban(m):
    user = users.process_user(m.from_user)
    if user['status'] == 'banned':
        return True


def arguments_lambda(m):
    return m.text.count(' ')


def promote_lambda(m):
    return owner_lambda(m) and m.text == promote_command and reply_lambda(m)


def reply_lambda(m):
    return m.reply_to_message


def wideban_lambda(m):
    return owner_lambda(m) and m.text == global_ban_command and reply_lambda(m)


def unwideban_lambda(m):
    return owner_lambda(m) and m.text == global_unban_command and reply_lambda(m)


def member_lambda(m):
    return owner_lambda(m) and m.text == grant_membership_command and reply_lambda(m)


def shana_lamda(m):
    return m.text.lower() in shana_commands and reply_lambda(m)


def ganyba_lamda(m):
    return m.text.lower() in ganyba_commands and reply_lambda(m)


def members_lambda(m):
    users.process_user(m.from_user)
    user = bot.get_chat_member(m.chat.id, m.from_user.id)
    if owner_lambda(m):
        return True
    if user.status == 'member':
        return True
    if user.status == 'admin':
        return True
    if user.status == 'creator':
        return True
    return False


def owner_lambda(m):
    return m.from_user.id in users.owners


def owner_callback(c):
    return c.from_user.id in users.owners


def join_request_callback(c):
    return (c.data.startswith('ja ') or c.data.startswith('jd '))


def butterfly(m):
    return owner_lambda(m) and m.text == allow_chat_command


def chat_admin_check(m):
    users.process_user(m.from_user)
    user = bot.get_chat_member(m.chat.id, m.from_user.id)
    if owner_lambda(m):
        return True
    if user.status == 'admin':
        return True
    if user.status == 'creator':
        return True
    return False


def user_check_lambda(m):
    users.process_user(m.from_user)
    if chat_admin_check(m):
        return
    if check_ban(m):
        bot.ban_chat_member(m.chat.id, m.from_user.id)


def chat_check_lambda(m):
    if m.chat.type == 'private':
        return False
    if butterfly(m):
        bot.send_message(log_channel, f'{allow_chat_command}✅`{m.chat.id}`|{m.chat.title}\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                         parse_mode='Markdown')
        chats.create_chat(m.chat.id, m.chat.title)
    if not m.chat.id in chats.chats:
        if m.new_chat_members:
            if m.new_chat_members[0].id == self_id:
                return False
        return True
