import datetime
import random
from typing import Optional

from collection.user import User, UserStatus, UserRole
from db import user_collection


class UserManager(object):
    def __init__(self):
        self.user_collection = user_collection

    def register(self, public_address: str) -> (bool, int):
        user_exists = self.user_collection.find_one({'public_address': public_address})

        if user_exists:
            return False, -1

        nonce = random.randint(10 ** 5, 10 ** 7)
        datetime_utc = datetime.datetime.utcnow()
        user: User = User(public_address=public_address, created_at=datetime_utc,
                          is_blocked=False, nonce=nonce, updated_at=datetime_utc, status=UserStatus.active,
                          roles=[UserRole.user])
        self.user_collection.insert_one(user)
        return True, nonce

    def get_nonce(self, public_address: str) -> int:
        user = self.user_collection.find_one({'public_address': public_address})

        if not user:
            return -1

        return user.get("nonce")

    def get_by_public_address(self, public_address: str) -> Optional[User]:
        user = self.user_collection.find_one({'public_address': public_address})
        return user


user_manager = UserManager()
