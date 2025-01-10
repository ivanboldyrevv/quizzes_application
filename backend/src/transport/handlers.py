from fastapi import APIRouter, Depends

from .request import RequestQuizResult, RequestToAddUser, RequestAddQuiz
from service_ import QuizService


quiz_route = APIRouter()


def q_service():
    return QuizService()


@quiz_route.post("/add_user")
async def add_user(user: RequestToAddUser, q_service: QuizService = Depends(q_service)):
    return q_service.add_user(user)


@quiz_route.get("/quizzes")
async def get_quizzes(q_service: QuizService = Depends(q_service)):
    return q_service.get_quizzes()


@quiz_route.get("/quiz/{quiz_id}")
async def get_quiz_by_id(quiz_id: str, q_service: QuizService = Depends(q_service)):
    return q_service.get_quiz_by_id(quiz_id)


@quiz_route.post("/add_quiz")
async def add_quiz(quiz: RequestAddQuiz, q_service: QuizService = Depends(q_service)):
    return q_service.add_quiz(quiz)


@quiz_route.post("/quiz_result")
async def quiz_result(quiz_result: RequestQuizResult, q_service: QuizService = Depends(q_service)):
    return q_service.add_quiz_result(quiz_result)


@quiz_route.get("/user_stats/{user_id}")
async def get_user_stats(user_id: str, q_service: QuizService = Depends(q_service)):
    return q_service.get_user_quiz_statistics(user_id)
