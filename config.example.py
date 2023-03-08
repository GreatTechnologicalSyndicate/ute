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

# Save your config in config.py

## DATABASE
mongo_url = 'mongodb://127.0.0.1:27017/?directConnection=true'  # dont change unless you know what are you doing
database_name = 'ute'  # you can customize this value

## TELEGRAM
telegram_token = 'bot token'
owners = [666, 777, 888]  # admin user ids
log_channel = -1007777777 # admin chat id

## COMMANDS
allow_chat_command = "🦋"
promote_command = '🪄🥑'
global_ban_command = '🔨🏛'
global_unban_command = '🕊🏛'
grant_membership_command = '🛂🏛'

members_codename = 'member'

shana_commands = ['шана', 'дяка', 'база', '+']
ganyba_commands = ['крінж', 'ганьба', 'на гілляку', '-']