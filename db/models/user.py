from mongoengine import StringField, IntField, Document, DictField, ListField


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
        tts += f'📈: {self.status}\n'
        tts += f'🐲: {self.reputation}\n'
        n = '\n'
        tts += f'{n.join(self.awards)}' if self.awards else ''
        return tts
        
    @property
    def banned(self):
        return self.status == 'banned'

