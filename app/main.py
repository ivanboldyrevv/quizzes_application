import uuid

from fastapi import FastAPI
from peewee import PostgresqlDatabase

from schemas import QuizSchema
from models import Quiz, Question, Option


db = PostgresqlDatabase("quiz_db", user="postgres", password="pass", host="db", port="5432")

db.connect()
db.drop_tables((Quiz, Option, Question))
db.create_tables([Quiz, Question, Option])

app = FastAPI()


def create_quiz():
    qid = str(uuid.uuid4())

    quiz = Quiz.create(quiz_id=qid, quizname="test_quiz")

    question = Question.create(question_id=uuid.uuid4(), question_text="test-question", quiz_id=quiz)

    Option.create(
        option_id=uuid.uuid4(),
        option_name="test",
        is_correct=True,
        question_id=question,
    )

    Option.create(
        option_id=uuid.uuid4(),
        option_name="test-2",
        is_correct=False,
        question_id=question,
    )


create_quiz()


@app.get("/quizzes")
async def get_quizzes():
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


@app.get("/quiz/{quiz_id}")
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


@app.post("/add_quiz/")
def add_quiz(quiz: QuizSchema):
    quiz_uuid = uuid.uuid4()
    new_quiz = Quiz.create(quiz_id=quiz_uuid, quizname=quiz.quiz_name)

    for question in quiz.questions:
        question = Question.create(question_id=uuid.uuid4(), question_text=question.question_text, quiz_id=new_quiz)

        for option in question.options:
            Option.create(option_id=uuid.uuid4(), option_name=option.option_text, is_correct=option.is_correct,
                          question_id=question)

    return [i for i in Quiz.select().where(Quiz.quiz_id == quiz_uuid)]


@app.delete("/delete_quiz/{quiz_id}")
def delete_quiz(quiz_id: uuid.UUID):
    quiz = Quiz.get(Quiz.quiz_id == quiz_id)
    if quiz.delete_instance(recursive=True):
        return {"error": "0"}
    return {"error": "1"}
