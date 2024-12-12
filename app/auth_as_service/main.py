from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel
from peewee import Model, UUIDField, CharField, PostgresqlDatabase


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


db = PostgresqlDatabase("quiz_db", user="postgres", password="pass", host="db", port="5432")
db.connect()

app = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TestUser(Model):
    uid = UUIDField(primary_key=True)
    username = CharField()
    password = CharField()

    class Meta:
        database = db


class RegistrationForm(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/register")
async def register_user(form: RegistrationForm):
    # TODO: username must be unique
    TestUser.create(uid=uuid.uuid4(), username=form.username, password=form.password)
    return "ok"


@app.post("/login")
async def authenticate_user(form: RegistrationForm):
    if (user := TestUser.select().where(TestUser.username == form.username)):
        return user


@app.post("/token")
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
