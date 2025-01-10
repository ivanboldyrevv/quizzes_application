import uuid

from typing import List
from pydantic import BaseModel


class OptionSchema(BaseModel):
    option_text: str
    is_correct: bool


class QuestionSchema(BaseModel):
    question_text: str
    options: List[OptionSchema]


class QuizSchema(BaseModel):
    quiz_name: str
    questions: List[QuestionSchema]


class OptionResponseSchema(BaseModel):
    option_id: uuid.UUID
    option_text: str
    is_correct: bool


class QuestionResponseSchema(BaseModel):
    question_id: uuid.UUID
    question_text: str
    options: List[OptionResponseSchema]


class UserResponseSchema(BaseModel):
    quiz_id: uuid.UUID
    quiz_name: str
    questions: List[QuestionResponseSchema]
