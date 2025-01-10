import uuid

from peewee import PeeweeException
from fastapi import HTTPException

from models import User
from transfer import TokenTransfer, CredentialsTransfer
from exceptions import AccessDenied, IncorrectTokenType
from jwt_utils import JwtToolkit

from jwt import DecodeError


class AuthService:
    def __init__(self, jwt_toolkit: JwtToolkit) -> None:
        self.jwt_: JwtToolkit = jwt_toolkit

    async def sign_up(self, user_credentials: CredentialsTransfer):
        try:
            user = User.create(uid=uuid.uuid4(), username=user_credentials.username, password=user_credentials.password)
        except PeeweeException:
            raise HTTPException()

        token = self._issue_token(user)
        return token

    async def sign_in(self, user_credentials: CredentialsTransfer):
        user = User.select().where(User.username == user_credentials.username).get()

        if not user:
            return
        if not (user.password == user_credentials.password):
            return

        token = self._issue_token(user)

        return token

    async def logout(self):
        pass

    def _issue_token(self, user: CredentialsTransfer) -> TokenTransfer:
        access_token, refresh_token = self.jwt_.issue_token(
            subject=str(user.uid), payload={"username": user.username}
        )
        return TokenTransfer(access_token, refresh_token)

    def verify_token(self, token):
        try:
            payload = self.jwt_.decode_token(token)
            if payload["type"] != "access":
                raise IncorrectTokenType("Access token expected!")
        except DecodeError:
            raise AccessDenied("Invalid token!")

        uid = payload.get("sub")
        user = User.select().where(User.uid == uid).get()

        if user is None:
            raise AccessDenied("User does not exists!")
