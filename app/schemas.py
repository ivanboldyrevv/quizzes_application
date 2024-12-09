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
