import uuid
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from peewee import PostgresqlDatabase
from schemas import QuizSchema, UserResponseSchema
from models import Quiz, Question, Option

from auth import validate_token


db = PostgresqlDatabase("quiz_db", user="postgres", password="pass", host="db", port="5432")
db.connect()

quiz = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@quiz.get("/test_jwt/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@quiz.get("/quizzes")
async def get_quizzes(token: Annotated[str, Depends(oauth2_scheme)]):
    await validate_token(token)

    quizzes = []

    for quiz in Quiz.select():
        quiz_dict = {
            "quiz_id": quiz.quiz_id,
            "quizname": quiz.quizname,
            "questions": []
        }

        for question in quiz.questions:
            question_dict = {
                "question_id": question.question_id,
                "options": [opt for opt in question.options.dicts()]
            }

            quiz_dict["questions"].append(question_dict)

        quizzes.append(quiz_dict)

    return quizzes


@quiz.get("/quiz/{quiz_id}")
async def get_quiz(quiz_id: uuid.UUID):
    quiz = Quiz.select().where(Quiz.quiz_id == quiz_id).get()

    quiz_dict = {
            "quiz_id": quiz.quiz_id,
            "quizname": quiz.quizname,
            "questions": []
        }

    for question in quiz.questions:
        question_dict = {
            "question_id": question.question_id,
            "options": [opt for opt in question.options.dicts()]
        }

        quiz_dict["questions"].append(question_dict)

    return quiz_dict


@quiz.post("/add_quiz/")
def add_quiz(quiz: QuizSchema):
    quiz_uuid = uuid.uuid4()
    new_quiz = Quiz.create(quiz_id=quiz_uuid, quizname=quiz.quiz_name)

    print(quiz)

    for question in quiz.questions:
        new_question = Question.create(question_id=uuid.uuid4(), question_text=question.question_text, quiz_id=new_quiz)

        for option in question.options:
            print(option)
            Option.create(option_id=uuid.uuid4(), option_name=option.option_text, is_correct=option.is_correct,
                          question_id=new_question)

    return [i for i in Quiz.select().where(Quiz.quiz_id == quiz_uuid)]


@quiz.delete("/delete_quiz/{quiz_id}")
def delete_quiz(quiz_id: uuid.UUID):
    quiz = Quiz.get(Quiz.quiz_id == quiz_id)
    if quiz.delete_instance(recursive=True):
        return {"error": "0"}
    return {"error": "1"}


@quiz.post("/check_quiz/")
def check_quiz(user_response: UserResponseSchema):
    questions = user_response.questions

    total_corrects = 0
    for question in questions:
        total_corrects += 1 if sum([i.is_correct for i in question.options if i]) else 0

    total_questions = len(questions)

    return (total_corrects / total_questions) * 100
