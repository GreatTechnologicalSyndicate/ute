from datetime import datetime
from threading import Thread
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from .lambdas import *


@bot.message_handler(func=chat_check_lambda)
def chat_check_handler(m):
    bot.leave_chat(m.chat.id)
    bot.send_message(log_channel, f'🦋❌`{m.chat.id}`|{m.chat.title}\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                     parse_mode='Markdown')


@bot.message_handler(func=user_check_lambda, content_types=['text', 'audio', 'photo', 'voice', 'video', 'document',
                                                            'text', 'location', 'contact', 'sticker',
                                                            'new_chat_members'])
def user_check_handler(m):
    pass


@bot.chat_join_request_handler()
def chat_join_request(r):
    kb = InlineKeyboardMarkup()

    tts = '📬Запрос на вступление в чат!\n'
    tts += f'🗺Чат: {r.chat.title}\n'
    tts += f'👤Пользователь: {bot.form_html_userlink(r.from_user.first_name, r.from_user.id)}'

    kb.add(InlineKeyboardButton('✅Принять', callback_data=f'ja {r.chat.id} {r.from_user.id}'))
    kb.add(InlineKeyboardButton('❌Отклонить', callback_data=f'jd {r.chat.id} {r.from_user.id}'))

    bot.send_message(log_channel, tts, parse_mode='HTML', reply_markup=kb)


@bot.callback_query_handler(func=join_request_callback)
def jc_handler(c):
    accept = True if c.data[1] == 'a' else False
    chat_id = int(c.data.split()[1])
    user_id = int(c.data.split()[2])
    m = c.message
    tts = m.text
    if accept:
        bot.approve_chat_join_request(chat_id, user_id)
        bot.edit_message_text(f'{tts}\n✅Принято!', m.chat.id, m.message_id, parse_mode='HTML')
    else:
        bot.decline_chat_join_request(chat_id, user_id)
        bot.edit_message_text(f'{tts}\n❌Отклонено!', m.chat.id, m.message_id, parse_mode='HTML')


@bot.message_handler(func=unwideban_lambda)
def wideban_handler(m):
    user = m.reply_to_message.from_user
    user = users.process_user(user)
    bot.respond_to(m, f'{m.text}✅')
    users.unban(user["_id"])
    for chat_id in chats.chats:
        chats.unban(chat_id, user['_id'])
        try:
            bot.unban_chat_member(chat_id, user['_id'])
        except:
            chat = chats.get_chat(chat_id)
            bot.send_message(log_channel, f'🔨❔ | {chat["title"]} | {chat["_id"]}')
    bot.send_message(log_channel, f'{m.text}✅ | `{user["_id"]}`\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                     parse_mode='Markdown')


@bot.message_handler(func=wideban_lambda)
def wideban_handler(m):
    user = m.reply_to_message.from_user
    user = users.process_user(user)
    bot.respond_to(m, f'{m.text}✅')
    users.ban(user["_id"])
    for chat_id in chats.chats:
        chats.ban(chat_id, user['_id'])
        try:
            bot.ban_chat_member(chat_id, user['_id'])
        except:
            chat = chats.get_chat(chat_id)
            bot.send_message(log_channel, f'🔨❔ | {chat["title"]} | {chat["_id"]}')
    bot.send_message(log_channel, f'{m.text}✅ | `{user["_id"]}`\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                     parse_mode='Markdown')


@bot.message_handler(func=promote_lambda)
def promote_handler(m):
    user = m.reply_to_message.from_user
    user = users.process_user(user)
    users.set_status(user['_id'], 'owner')
    bot.send_message(log_channel,
                     f'{m.text}✅ | `{user["_id"]}` | `{m.chat.id}`\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                     parse_mode='Markdown')


@bot.message_handler(func=member_lambda)
def member_handler(m):
    user = m.reply_to_message.from_user
    user = users.process_user(user)
    users.set_status(user['_id'], 'member')
    bot.send_message(log_channel,
                     f'{m.text}✅ | `{user["_id"]}` | `{m.chat.id}`\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                     parse_mode='Markdown')


@bot.message_handler(func=lambda m: members_lambda(m) and shana_lamda(m))
def shana_handler(m):
    if m.from_user.id == m.reply_to_message.from_user.id:
        bot.respond_to(m, 'Choose a human please (not yourself)')
        return
    communicator = users.process_user(m.from_user)
    time_now = int(datetime.utcnow().timestamp())
    cooldown_time = 1000 * 60 * 60
    time_differ = time_now - int(communicator['reputation_cooldown'])
    if time_differ < cooldown_time:
        bot.respond_to(m, f"Wait for {datetime.fromtimestamp(cooldown_time - time_differ).strftime('%H:%M:%S')}")
        return

    user = m.reply_to_message.from_user
    user = users.process_user(user)
    users.set_reputation(user['_id'], user['reputation'] + 1)
    users.set_reputation_cooldown(communicator['_id'], time_now)

    bot.respond_to(m, f'🆙 {user["name"]} +1 rep')


@bot.message_handler(func=lambda m: members_lambda(m) and ganyba_lamda(m))
def ganyba_handler(m):
    if m.from_user.id == m.reply_to_message.from_user.id:
        bot.respond_to(m, 'Choose a human please (not yourself)')
        return
    communicator = m.from_user
    communicator = users.process_user(communicator)
    time_now = int(datetime.utcnow().timestamp())
    cooldown_time = 1000 * 60 * 60
    time_differ = time_now - int(communicator['reputation_cooldown'])
    if time_differ < cooldown_time:
        bot.respond_to(m, f"Wait for {datetime.fromtimestamp(cooldown_time - time_differ).strftime('%H:%M:%S')}")
        return

    user = m.reply_to_message.from_user
    user = users.process_user(user)
    users.set_reputation(user['_id'], user['reputation'] - 1)
    users.set_reputation_cooldown(communicator['_id'], time_now)

    bot.respond_to(m, f'🔽 {user["name"]} -1 rep')


@bot.message_handler(commands=['achievement'],
                     func=lambda m: owner_lambda(m) and arguments_lambda(m) and reply_lambda(m))
def achievement_handler(m):
    name = m.text.split(' ', 1)[1]
    user = m.reply_to_message.from_user
    user = users.process_user(user)
    awards = user['awards']
    awards.append(name)
    users.set_awards(user['_id'], awards)


@bot.message_handler(commands=['globalban'], func=lambda m: owner_lambda(m) and arguments_lambda(m))
def globalban_handler(m):
    user_id = int(m.text.split(' ', 1)[1])
    user = users.get_user(user_id)
    bot.respond_to(m, f'{m.text}✅')
    users.ban(user["_id"])
    for chat_id in chats.chats:
        chats.ban(chat_id, user['_id'])
        try:
            bot.ban_chat_member(chat_id, user['_id'])
        except:
            chat = chats.get_chat(chat_id)
            bot.send_message(log_channel, f'🔨❔ | {chat["title"]} | {chat["_id"]}')
    bot.send_message(log_channel, f'{m.text}✅ | `{user["_id"]}`\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                     parse_mode='Markdown')


@bot.message_handler(commands=['map'], func=owner_lambda)
def map_handler(m):
    tts = '🗺Карта чатов:\n'
    for chat_id in chats.chats:
        chat = chats.get_chat(chat_id)
        try:
            link = bot.export_chat_invite_link(chat_id)
        except:
            link = '0.0.0.0/error'
        tts += f'<a href="{link}">{chat["title"]}</a> - {chat["_id"]}\n'
    bot.respond_to(m, tts, parse_mode='HTML')


@bot.message_handler(commands=['banlist'], func=owner_lambda)
def map_handler(m):
    tts = '🔨Список забубленных челов:\n'
    for user in users.get_users():
        if user['status'] == 'banned':
            tts += f'{bot.form_html_userlink(user["name"], user["_id"])}\n'
    bot.respond_to(m, tts, parse_mode='HTML')


@bot.message_handler(commands=['members'], func=owner_lambda)
def map_handler(m):
    tts = '🛂Список граждан:\n'
    for user in users.get_users():
        if user['status'] == 'member' or user['status'] == 'owner':
            tts += f'{bot.form_html_userlink(user["name"], user["_id"])}\n'
    bot.respond_to(m, tts, parse_mode='HTML')


@bot.message_handler(commands=['profile'])
def profile_handler(m):
    user = m.from_user
    if m.reply_to_message:
        user = m.reply_to_message.from_user
    user = users.process_user(user)
    tts = f'👤User profile {user["name"]}:\n'
    tts += f'🆔: {user["_id"]}\n'
    tts += f'📈Status: {user["status"]}\n'
    tts += f'🐲Reputation: {user["reputation"]}\n'
    tts += f'🏆Achievements: \n{", ".join(user["awards"])}'

    bot.respond_to(m, tts)


@bot.message_handler(commands=['owners'])
def owners_handler(m):
    tts = ''

    for owner in users.get_owners():
        tts += f"{owner['name']}: `{owner['_id']}`\n"

    bot.respond_to(m, tts, parse_mode="Markdown")


@bot.message_handler(commands=['admins'])
def admins_handler(m):
    tts = ''

    for admin in users.get_admins():
        tts += f"{admin['name']}: `{admin['_id']}`\n"

    bot.respond_to(m, tts, parse_mode="Markdown")


@bot.message_handler(commands=['start'])
def start_handler(m):
    bot.respond_to(m, 'Greetings!')


bot.send_message(log_channel, '♻️✅')
Thread(target=bot.infinity_polling).start()
