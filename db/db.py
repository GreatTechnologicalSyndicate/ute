from .models.user import User
from .models.chat import Chat
from .models import status

from config import members_codename, owners, database_name
from mongoengine import connect


class Database:
    def __init__(self, mongo_url: str):
        self.connection = connect(host=mongo_url, db=database_name)
        self.User = User
        self.Chat = Chat

        for owner in owners:
            user = self.get_user(owner)
            user.status = status.OWNER
            user.save()

    def get_chats(self):
        return Chat.objects()

    @property
    def chats(self):
        return Chat.objects.distinct('id')

    def delete_chat(self, chat_id: int):
        Chat.objects(id=chat_id).delete()

    def create_chat(self, chat_id: int, title: str) -> Chat:
        Chat.objects(id=chat_id).update_one(upsert=True, title=title)
        return Chat.objects.get(id=chat_id)

    def get_chat(self, chat_id: int) -> Chat:
        return Chat.objects.get(id=chat_id)

    def get_users(self) -> list[User]:
        return User.objects()

    def get_top_reputation(self):
        i = 0
        for user in User.objects.order_by('-reputation').limit(10):
            i += 1
            yield user, 1

    @property
    def owners(self) -> list[int]:
        return User.objects.filter(status=status.OWNER).distinct('id')

    def get_owners(self) -> list[User]:
        return User.objects(status=status.OWNER)

    def get_members(self) -> list[User]:
        return User.objects(status=members_codename)

    def get_user(self, user_id: int, name='null') -> User:
        user = User.objects(id=user_id).update_one(upsert=True, name=name)
        return User.objects.get(id=user_id)

    def set_status(self, user_id: int, value: str) -> User:
        return self.get_user(user_id).set_status(value)

    def ban_user(self, user_id: int) -> None:
        self.set_status(user_id, status.BANNED)

    def unban_user(self, user_id: int) -> None:
        self.set_status(user_id, status.GUEST)

    def create_user(self, user_id: int, name='null') -> User:
        user = User(id=user_id, name=name)
        return user.save()

    def process_tg_user(self, tg_user) -> User:
        return self.get_user(tg_user.id, tg_user.first_name)
