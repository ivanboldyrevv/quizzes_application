from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transport.handlers import quiz_route


app = FastAPI(openapi_url="/api/v1/quizzes/openapi.json", docs_url="/api/v1/quizzes/docs")
app.include_router(quiz_route, prefix="/api/v1/quizzes")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
