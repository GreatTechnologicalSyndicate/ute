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

