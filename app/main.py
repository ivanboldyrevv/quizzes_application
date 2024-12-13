from fastapi import FastAPI
from service import quiz


app = FastAPI(openapi_url="/api/v1/quizzes/openapi.json", docs_url="/api/v1/quizzes/docs")
app.include_router(quiz, prefix="/api/v1/quizzes")
