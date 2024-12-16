from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from transport.handlers import auth_router


app = FastAPI(openapi_url="/api/v1/oauth2/openapi.json", docs_url="/api/v1/oauth2/docs")


origins = [
    "http://localhost:8080",
    "http://localhost:8002",
    "http://localhost:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/oauth2")
