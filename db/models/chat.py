from mongoengine import StringField, IntField, Document, ListField


class Chat(Document):
    id = IntField(primary_key=True)
    title = StringField()
    banned = ListField()
    administrators = ListField()

    meta = {
        'collection': 'chats'
    }
