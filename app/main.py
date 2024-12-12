from fastapi import FastAPI

from auth import auth
from quiz import quiz


app = FastAPI()

app.include_router(auth)
app.include_router(quiz)
