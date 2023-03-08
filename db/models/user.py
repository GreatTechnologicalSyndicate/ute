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

from mongoengine import StringField, IntField, Document, DictField, ListField

from . import status


class User(Document):
    id = IntField(primary_key=True)
    name = StringField()
    status = StringField(default='guest')
    reputation = IntField(default=0)
    reputation_cooldown = IntField(default=0)
    money = IntField(default=0)
    stats = DictField()
    awards = ListField()

    meta = {
        'collection': 'users'
    }

    def profile(self):
        tts = f'👤: {self.name}\n'
        tts += f'🆔: {self.id}\n'
        tts += f'📈: {self.emoji}{self.status}\n'
        tts += f'🐲: {self.reputation}\n'
        n = '\n'
        tts += f'{n.join(self.awards)}' if self.awards else ''
        return tts

    def link(self):
        return f'<a href="tg://user?id={self.id}">{self.name}</a>'

    def is_status(self, value):
        if value == status.MEMBER:
            return self.status in [status.MEMBER, status.OWNER]
        elif value == status.GUEST:
            return self.status in [status.GUEST, status.MEMBER, status.OWNER]
        else:
            return value == self.status

    @property
    def emoji(self):
        return status.emoji.get(self.status, '👤')

    def unban(self):
        return self.set_status(status.GUEST)

    def ban(self):
        return self.set_status(status.BANNED)

    def add_award(self, award: str):
        self.awards.append(award)
        return self.save()

    def set_status(self, value: str):
        self.status = value
        return self.save()

    @property
    def banned(self):
        return self.status == status.BANNED

    @property
    def owner(self) -> bool:
        return self.status == status.OWNER

    @property
    def member(self) -> bool:
        return self.status == status.OWNER or self.status == status.MEMBER

