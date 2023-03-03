from .models.user import User
from .models.chat import Chat

from config import members_codename, owners, database_name
from mongoengine import connect


class Database:
    def __init__(self, mongo_url):
        self.connection = connect(host=mongo_url, db=database_name)
        self.User = User
        self.Chat = Chat

        for owner in owners:
            user = self.get_user(owner)
            user.status = 'owner'
            user.save()

    def get_chats(self):
        return Chat.objects()

    @property
    def chats(self):
        return Chat.objects.distinct('id')

    def delete_chat(self, chat_id):
        Chat.objects(id=chat_id).delete()

    def create_chat(self, chat_id, title):
        print(f'Butterflying: {chat_id}')
        chat = Chat.objects(id=chat_id).update_one(upsert=True, title=title)
        return Chat.objects.get(id=chat_id)

    def get_chat(self, chat_id: int):
        return Chat.objects.get(id=chat_id)

    def get_users(self):
        return User.objects()

    def get_top_reputation(self):
        return User.objects.order_by('-reputation').limit(10)

    @property
    def owners(self):
        return User.objects.filter(status='owner').distinct('id')

    def get_owners(self):
        return User.objects(status='owner')

    def get_members(self):
        return User.objects(status=members_codename)

    def get_user(self, user_id: int, name='null') -> User:
        user = User.objects(id=user_id).update_one(upsert=True, name=name)
        return User.objects.get(id=user_id)

    def set_status(self, user_id: int, status: str):
        User.objects(id=user_id).update_one(set__status=status)

    def ban_user(self, user_id: int):
        self.set_status(user_id, 'banned')

    def unban_user(self, user_id):
        self.set_status(user_id, 'guest')

    def create_user(self, user_id: int, name='null') -> User:
        user = User(id=user_id, name=name)
        return user.save()

    def process_tg_user(self, tg_user) -> User:
        return self.get_user(tg_user.id, tg_user.first_name)
