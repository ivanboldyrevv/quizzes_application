import httpx
import pytest
import uuid
from datetime import datetime

from fastapi import status

from models import User, Quiz, Question, Option, UserQuizStatistics
from peewee import PostgresqlDatabase

from transport.request import RequestAddQuiz
from service_ import QuizService


AUTH_URL = "http://localhost:8001/api/v1/oauth2"
QUIZ_APP_URL = "http://localhost:8002/api/v1/quizzes"


@pytest.fixture(scope="session", autouse=True)
def initialize_test_database():
    MODELS = [User, Quiz, Question, Option, UserQuizStatistics]

    database_config = {
        "user": "auth-dev",
        "password": "pass",
        "host": "localhost",
        "port": "5434",
        "database": "test"
    }

    test_environment = PostgresqlDatabase(**database_config)

    test_environment.bind(MODELS, bind_refs=True, bind_backrefs=True)

    test_environment.connect()
    test_environment.create_tables(MODELS)

    yield

    test_environment.drop_tables(MODELS)
    test_environment.close()


@pytest.fixture(scope="session")
def mock_user() -> User:
    user_id = uuid.uuid4()
    u = User.create(user_id=user_id, username="test-username")
    return u


@pytest.fixture(scope="session")
def service() -> QuizService:
    return QuizService()


def test_add_quiz(service, mock_user):
    req_data = {
        "quiz_name": "test",
        "questions":
        [
            {
                "question_text": "test-question-1",
                "options": [
                    {"option_text": "test-option-1", "is_correct": True},
                    {"option_text": "test-option-2", "is_correct": False}
                ]
            },
            {
                "question_text": "test-question-2",
                "options": [
                    {"option_text": "test-option-11", "is_correct": True},
                    {"option_text": "test-option-22", "is_correct": False}
                ]
            }
        ],
        "difficult_level": "easy",
        "created_by": str(mock_user.user_id)
    }

    result = service.add_quiz(RequestAddQuiz(**req_data))

    assert result.quiz_name == req_data["quiz_name"]
    assert result.created_by_id == mock_user
    assert result.creation_date is not None
    assert isinstance(result.creation_date, datetime) is True

    for index, question in enumerate(result.questions):
        request_current_question = req_data["questions"][index]
        assert question.question_text == request_current_question["question_text"]

        for index, option in enumerate(question.options):
            request_current_option = request_current_question["options"][index]
            assert option.option_text == request_current_option["option_text"]
            assert option.is_correct == request_current_option["is_correct"]


@pytest.fixture(scope="session")
def jwt_token():
    data = {"username": "test", "password": "test"}
    response = httpx.post(AUTH_URL + "/sign_in", json=data)
    json = response.json()
    return json["access_token"]


def test_get_quizzes():
    expected = [
            {"quiz_id": "a69d46d4-affb-4708-8819-42793c19ed80",
             "quizname": "test-quiz",
             "questions": [
                    {"question_id": "a69d46d4-affb-4708-8819-42793c19ed81",
                     "question_text": "test-question-1",
                     "option": [{"option_id": "a69d46d4-affb-4708-8819-42793c19ed90",
                                 "option_name": "test-option-1",
                                 "is_correct": False},
                                {"option_id": "a69d46d4-affb-4708-8819-42793c19ed91",
                                 "option_name": "test-option-2",
                                 "is_correct": True}]},
                    {"question_id": "a69d46d4-affb-4708-8819-42793c19ed82",
                     "question_text": "test-question-2",
                     "option": [{"option_id": "a69d46d4-affb-4708-8819-42793c19ed92",
                                 "option_name": "test-option-3",
                                 "is_correct": False},
                                {"option_id": "a69d46d4-affb-4708-8819-42793c19ed93",
                                 "option_name": "test-option-4",
                                 "is_correct": False},
                                {"option_id": "a69d46d4-affb-4708-8819-42793c19ed94",
                                 "option_name": "test-option-5",
                                 "is_correct": True}]},
                    {"question_id": "a69d46d4-affb-4708-8819-42793c19ed83",
                     "question_text": "test-question-3",
                     "option": [{"option_id": "a69d46d4-affb-4708-8819-42793c19ed95",
                                 "option_name": "test-option-6",
                                 "is_correct": False},
                                {"option_id": "a69d46d4-affb-4708-8819-42793c19ed96",
                                 "option_name": "test-option-7",
                                 "is_correct": True}]}]},

            {"quiz_id": "a69d46d4-affb-4708-8819-42793c19ed50",
             "quizname": "test-quiz-2",
             "questions": [
                        {"question_id": "a69d46d4-affb-4708-8819-42793c19ed11",
                         "question_text": "test-question-2-1",
                         "option": [
                                {"option_id": "a69d46d4-affb-4708-8819-42793c19ed31",
                                 "option_name": "test-option-2-1",
                                 "is_correct": False},
                                {"option_id": "a69d46d4-affb-4708-8819-42793c19ed32",
                                 "option_name": "test-option-2-2",
                                 "is_correct": True}]
                         }]}]
    response = httpx.get(QUIZ_APP_URL + "/quizzes")
    json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert json == expected


def test_get_quiz_by_id():
    expected = {"quiz_id": "a69d46d4-affb-4708-8819-42793c19ed50",
                "quizname": "test-quiz-2",
                "questions": [
                    {"question_id": "a69d46d4-affb-4708-8819-42793c19ed11",
                     "question_text": "test-question-2-1",
                     "option": [{"option_id": "a69d46d4-affb-4708-8819-42793c19ed31",
                                 "option_name": "test-option-2-1",
                                 "is_correct": False},
                                {"option_id": "a69d46d4-affb-4708-8819-42793c19ed32",
                                 "option_name": "test-option-2-2",
                                 "is_correct": True}]
                     }]
                }
    response = httpx.get(QUIZ_APP_URL + "/quiz/a69d46d4-affb-4708-8819-42793c19ed50")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected
