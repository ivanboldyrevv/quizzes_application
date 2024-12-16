import jwt
import uuid

from datetime import timedelta, datetime, timezone
from typing import Any, Dict

from .config import JwtConfig


class JwtToolkit:
    def __init__(self, config: JwtConfig) -> None:
        self._config: JwtConfig = config

    def issue_token(self, subject: str, payload: Dict[str, Any] = {}, ttl: timedelta = None):
        """
            Call to generate access_token and refresh_token.

            args:
                subject: the subject to whom the token is issued
                payload: payload that you want to add to the token
                ttl: token time to live

            returns:
                a tuple with tokens. i = 0 - access_token, i = 1 - refresh_token
        """
        access_token = self._create_access_token(subject, payload, ttl)
        refresh_token = self._create_refresh_token(subject, payload, ttl)

        return access_token, refresh_token

    def _create_access_token(self, subject: str, payload: Dict[str, Any] = {}, ttl: timedelta = None) -> str:
        return self._sign_token("access", subject, payload, ttl)

    def _create_refresh_token(self, subject: str, payload: Dict[str, Any] = {}, ttl: timedelta = None) -> str:
        return self._sign_token("refresh", subject, payload, ttl)

    def _sign_token(self, type: str, subject: str, payload: Dict[str, Any] = {}, ttl: timedelta = None) -> str:
        """
            Token creation logic.

            args:
                type: token type(access/refresh)
                subject: the subject to whom the token is issued
                payload: payload that you want to add to the token
                ttl: token time to live

            returns:
                encoded token
        """

        current_timestamp = datetime.now(tz=timezone.utc).timestamp()

        data = dict(
            iss="@auth_service",
            sub=subject,
            type=type,
            jti=str(uuid.uuid4()),  # token uuid
            iat=current_timestamp,  # token issuance time
            nbf=payload["nbf"] if payload.get("nbf") else current_timestamp
        )

        data.update(dict(exp=data["nbf"] + int(ttl.total_seconds()))) if ttl else None
        payload.update(data)

        return jwt.encode(payload=payload, key=self._config.secret, algorithm=self._config.algorithm)

    def decode_token(self, token):
        return jwt.decode(token, self._config.secret, self._config.algorithm)
