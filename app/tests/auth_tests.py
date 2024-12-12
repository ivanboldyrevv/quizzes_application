import jwt
import httpx

from fastapi import status
from datetime import datetime, timedelta, timezone


SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def test_valid_token():
    response = httpx.post("http://localhost:8080/token", data={"username": "test", "password": "test"})
    print(response.json())
    assert response.status_code == status.HTTP_200_OK


def test_non_valid_token():
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": "unexisted_user"}, expires_delta=access_token_expires)

    response = httpx.post("http://localhost:8080/validate_token/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
