from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import List


class RequestToAddUser(BaseModel):
    user_id: UUID
    username: str


class Option(BaseModel):
    option_text: str
    is_correct: bool


class Question(BaseModel):
    question_text: str
    options: List[Option]


class RequestAddQuiz(BaseModel):
    quiz_name: str
    questions: List[Question]
    difficult_level: str
    created_by: str


class RequestQuizResult(BaseModel):
    user_id: UUID
    quiz_id: UUID
    dispatch_date: datetime
    accept_percent: float
