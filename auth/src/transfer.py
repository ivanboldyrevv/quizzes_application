from uuid import UUID
from dataclasses import dataclass


@dataclass
class TokenTransfer:
    access_token: str
    refresh_token: str


@dataclass
class CredentialsTransfer:
    username: str
    password: str


@dataclass
class UserTransfer:
    uid: UUID
    username: str
