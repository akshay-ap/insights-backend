from datetime import datetime
from enum import Enum
from typing import TypedDict, List


class UserStatus(str, Enum):
    deleted = 'deleted'
    active = 'active'


class UserRole(str, Enum):
    user = 'user'
    admin = 'admin'


class User(TypedDict):
    public_address: str
    created_at: datetime
    is_blocked: bool
    updated_at: datetime
    status: str
    roles: List[UserRole]
    nonce: int
