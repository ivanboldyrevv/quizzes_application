import uuid
from typing import Annotated
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError


from fastapi import Depends, HTTPException, status, APIRouter, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models import User
from schemas import RegistrationForm, Token, TokenData


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


auth = APIRouter()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@auth.get("/")
async def index():
    return {"hello": "ok"}


@auth.post("/verify_token")
async def verify_token(request: Request):
    token = request.headers["Authorization"].split()[1]
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        # detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    # user = User.get(User.username == token_data.username).__dict__
    # if user is None:
        # raise credentials_exception

    return token_data


@auth.post("/register/")
async def register_user(form: RegistrationForm):
    # TODO: username must be unique
    User.create(uid=uuid.uuid4(), username=form.username, password=form.password)
    return "ok"


@auth.post("/authenticate/")
async def authenticate_user(form: RegistrationForm):
    # user = [i for i in User.select().where(User.username == form.username).dicts()]
    # if user:
        # return user[0]
    return {"username": "yos"}


@auth.post("/token/")
async def login_for_access_token(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(form)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")
