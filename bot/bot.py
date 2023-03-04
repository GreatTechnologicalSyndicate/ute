import time
from datetime import datetime
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from .lambdas import *


@bot.message_handler(func=chat_check_lambda)
def chat_check_handler(m):
    try:
        bot.leave_chat(m.chat.id)
    except:
        return
    bot.send_message(log_channel,
                     f'{allow_chat_command}❌`{m.chat.id}`|{m.chat.title}\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                     parse_mode='Markdown')


@bot.message_handler(func=user_check_lambda, content_types=['text', 'audio', 'photo', 'voice', 'video', 'document',
                                                            'text', 'location', 'contact', 'sticker',
                                                            'new_chat_members'])
def user_check_handler(m):
    pass


@bot.chat_join_request_handler()
def chat_join_request(r):
    kb = InlineKeyboardMarkup()

    tts = '📬💬!\n'
    tts += f'🗺💬: {r.chat.title}\n'
    tts += f'👤: {bot.form_html_userlink(r.from_user.first_name, r.from_user.id)}'

    kb.add(InlineKeyboardButton('✅', callback_data=f'ja {r.chat.id} {r.from_user.id}'))
    kb.add(InlineKeyboardButton('❌', callback_data=f'jd {r.chat.id} {r.from_user.id}'))

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
def unban_handler(m):
    user = db.process_tg_user(m.reply_to_message.from_user)
    bot.respond_to(m, f'{m.text}✅')
    db.unban_user(user.id)
    for chat_id in db.chats:
        try:
            bot.unban_chat_member(chat_id, user.id)
        except:
            chat = db.get_chat(chat_id)
            bot.send_message(log_channel, f'🔨❔ | {chat.title} | {chat.id}')
    bot.send_message(log_channel, f'{m.text}✅ | `{user.id}`\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                     parse_mode='Markdown')


@bot.message_handler(func=wideban_lambda)
def ban_handler(m):
    user = db.process_tg_user(m.reply_to_message.from_user)
    bot.respond_to(m, f'{m.text}✅')
    db.ban_user(user.id)
    for chat_id in db.chats:
        try:
            bot.ban_chat_member(chat_id, user.id)
        except:
            chat = db.get_chat(chat_id)
            bot.send_message(log_channel, f'🔨❔ | {chat.title} | {chat.id}')
    bot.send_message(log_channel, f'{m.text}✅ | `{user.id}`\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                     parse_mode='Markdown')


@bot.message_handler(func=promote_lambda)
def promote_handler(m):
    user = db.process_tg_user(m.reply_to_message.from_user)
    user.status = 'owner'
    user.save()
    bot.send_message(log_channel,
                     f'{m.text}✅ | `{user.id}` | `{m.chat.id}`\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                     parse_mode='Markdown')


@bot.message_handler(func=member_lambda)
def member_handler(m):
    user = db.process_tg_user(m.reply_to_message.from_user)
    user.status = members_codename
    user.save()
    bot.send_message(log_channel,
                     f'{m.text}✅ | `{user.id}` | `{m.chat.id}`\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                     parse_mode='Markdown')


@bot.message_handler(func=lambda m: members_lambda(m) and shana_lamda(m))
def shana_handler(m):
    if m.from_user.id == m.reply_to_message.from_user.id or m.reply_to_message.from_user.is_bot:
        bot.respond_to(m, 'Choose a human please (not yourself)')
        return
    communicator = db.process_tg_user(m.from_user)
    time_now = time.time()
    cooldown_time = 3*60*60
    time_differ = time_now - communicator.reputation_cooldown
    if time_differ < cooldown_time:
        hours, remainder = divmod(cooldown_time - time_differ, 3600)  # 3600 seconds in an hour
        minutes, seconds = divmod(remainder, 60)  # 60 seconds in a minute
        bot.respond_to(m, f"Wait for {int(hours)}:{int(minutes)}:{int(seconds)}")
        return

    user = db.process_tg_user(m.reply_to_message.from_user)
    user.reputation += 1
    communicator.reputation_cooldown = time_now
    user.save()
    communicator.save()

    bot.respond_to(m, f'🆙 {user.name} +1 rep')


@bot.message_handler(func=lambda m: members_lambda(m) and ganyba_lamda(m))
def ganyba_handler(m):
    if m.from_user.id == m.reply_to_message.from_user.id or m.reply_to_message.from_user.is_bot:
        bot.respond_to(m, 'Choose a human please (not yourself)')
        return
    communicator = db.process_tg_user(m.from_user)
    time_now = time.time()
    cooldown_time = 3 * 60 * 60
    time_differ = time_now - int(communicator.reputation_cooldown)
    if time_differ < cooldown_time:
        hours, remainder = divmod(cooldown_time - time_differ, 3600)  # 3600 seconds in an hour
        minutes, seconds = divmod(remainder, 60)  # 60 seconds in a minute
        bot.respond_to(m, f"Wait for {hours}:{minutes}:{seconds}")
        return

    user = db.process_tg_user(m.reply_to_message.from_user)
    user.reputation -= 1
    communicator.reputation_cooldown = time_now
    user.save()
    communicator.save()

    bot.respond_to(m, f'🔽 {user["name"]} -1 rep')


@bot.message_handler(commands=['achievement'],
                     func=lambda m: owner_lambda(m) and arguments_lambda(m) and reply_lambda(m))
def achievement_handler(m):
    award = m.text.split(' ', 1)[1]
    user = db.process_tg_user(m.reply_to_message.from_user)
    user.awards.append(award)
    user.save()
    bot.reply_to(m, '🏆✅')


@bot.message_handler(commands=['global_ban'], func=lambda m: owner_lambda(m) and arguments_lambda(m))
def global_ban_handler(m):
    user_id = int(m.text.split(' ', 1)[1])
    user = db.get_user(user_id)
    bot.respond_to(m, f'{m.text}✅')
    db.ban_user(user_id)
    for chat_id in db.chats:
        try:
            bot.ban_chat_member(chat_id, user_id)
        except:
            chat = db.get_chat(chat_id)
            bot.send_message(log_channel, f'🔨❔ | {chat.title} | {chat.id}')
    bot.send_message(log_channel, f'{m.text}✅ | `{user.id}`\n\n{bot.form_html_messagelink(m, "🔍🔍🔍")}',
                     parse_mode='Markdown')


@bot.message_handler(commands=['map'], func=owner_lambda)
def map_handler(m):
    tts = '🗺📃:\n'
    for chat_id in db.chats:
        chat = db.get_chat(chat_id)
        try:
            link = bot.export_chat_invite_link(chat_id)
        except:
            link = '0.0.0.0/error'
        tts += f'<a href="{link}">{chat.title}</a> - {chat.id}\n'
    bot.respond_to(m, tts, parse_mode='HTML')


@bot.message_handler(commands=['banlist'], func=owner_lambda)
def map_handler(m):
    tts = '🔨📃:\n'
    for user in db.User.objects(status='banned'):
        tts += f'{bot.form_html_userlink(user.name, user.id)}\n'
    bot.respond_to(m, tts, parse_mode='HTML')


@bot.message_handler(commands=['rep'], func=members_lambda)
def map_handler(m):
    tts = '🔂📃:\n'
    i = 1
    for user in db.get_top_reputation():
        emoji = {members_codename: '🛂', 'owner': '👩🏻‍💼', 'guest': '👤', 'banned': '🚱'}.get(user.status, '👤')
        tts += f'{i}.{emoji}{user.name} - {user.reputation}\n'
        i += 1
    bot.respond_to(m, tts, parse_mode='HTML')


@bot.message_handler(commands=[members_codename+'s'], func=owner_lambda)
def members_handler(m):
    tts = '🛂📃:\n'
    for user in db.get_users():
        if user.status == members_codename or user.status == 'owner':
            tts += f'{bot.form_html_userlink(user.name, user.id)}\n'
    bot.respond_to(m, tts, parse_mode='HTML')


@bot.message_handler(commands=['profile'])
def profile_handler(m):
    user = m.from_user
    if m.reply_to_message:
        user = m.reply_to_message.from_user
    user = db.process_tg_user(user)
    bot.respond_to(m, user.profile())


@bot.message_handler(commands=['owners'])
def owners_handler(m):
    tts = ''

    for owner in db.get_owners():
        tts += f"{owner.name}: `{owner.id}`\n"

    bot.respond_to(m, tts, parse_mode="Markdown")


@bot.message_handler(commands=['start'])
def start_handler(m):
    bot.respond_to(m, '👋')


