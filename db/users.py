class Users:
    def __init__(self, db):
        self.db = db.users
        self.database = db

    def get_users(self):
        return self.db.find({})

    @property
    def owners(self):
        return [user['_id'] for user in self.db.find({'status': 'owner'})]

    def get_admins(self):
        return [user for user in self.db.find({'status': 'admin'})]

    def get_owners(self):
        return [user for user in self.db.find({'status': 'owner'})]

    def get_citizens(self):
        return [user for user in self.db.find({'status': 'members'})]

    def ban(self, user_id):
        self.set_status(user_id, 'banned')

    def unban(self, user_id):
        self.set_status(user_id, 'guest')

    def create_user(self, user_id: int, name='Без имени'):
        user = self.form_user_doc(user_id, name)
        self.db.insert_one(user)
        return user

    def set_status(self, user_id: int, status: str):
        self.db.update_one({'_id': user_id}, {'$set': {'status': status}})

    def set_reputation(self, user_id: int, reputation):
        self.db.update_one({'_id': user_id}, {'$set': {'reputation': reputation}})

    def set_awards(self, user_id: int, awards):
        self.db.update_one({'_id': user_id}, {'$set': {'awards': awards}})

    
    def set_reputation_cooldown(self, user_id: int, date: int):
        self.db.update_one({'_id': user_id}, {'$set': {'reputation_cooldown': date}})

    def set_name(self, user_id: int, name: str):
        self.db.update_one({'_id': user_id}, {'$set': {'name': name}})
    
    def get_user(self, user_id: int):
        user = self.db.find_one({'_id': user_id})
        if not user:
            self.create_user(user_id)
            user = self.db.find_one({'_id': user_id})
        return user

    def process_user(self, tg_user):
        user = self.get_user(tg_user.id)
        if not user:
            return self.create_user(tg_user.id, tg_user.first_name)
        self.set_name(tg_user.id, tg_user.first_name)
        return user

    def set_money(self, tg_user, count=0):
        user = self.process_user(tg_user.id, tg_user.name)

    def form_user_doc(self, user_id: int, name: str):
        return {
            '_id': user_id,
            'name': name,
            'money': 0,
            'reputation': 0,
            'reputation_cooldown': 0,
            'stats': {},
            'awards': [],
            'act': 0,
            'status': 'guest'
        }
