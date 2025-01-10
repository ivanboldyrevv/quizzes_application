import uuid
from datetime import datetime

from peewee import fn

from models import Quiz, Question, Option, User, UserQuizStatistics
from dto import QuizData, QuestionData, OptionData, UserStats, ExecutedQuiz
from transport.request import RequestQuizResult, RequestToAddUser


class QuizService:
    def add_user(self, user: RequestToAddUser):
        new_user = User.create(user_id=user.user_id, username=user.username)
        return new_user

    def get_quizzes(self):
        quizzes = []

        try:
            for quiz in Quiz.select(Quiz, User.username).join(User):
                curr = QuizData(quiz_id=quiz.quiz_id,
                                quiz_name=quiz.quiz_name,
                                difficult_level=quiz.difficult_level,
                                created_by=quiz.created_by_id.username,
                                creation_date=quiz.creation_date)
                self.iterate_questions(quiz.questions, curr.questions)
                quizzes.append(curr)
        except Exception as e:
            raise e

        return quizzes

    def get_quiz_by_id(self, quiz_id):
        quiz = Quiz.select().where(Quiz.quiz_id == quiz_id).get()
        needed = QuizData(quiz_id=quiz.quiz_id,
                          quiz_name=quiz.quiz_name,
                          difficult_level=quiz.difficult_level,
                          creation_date=quiz.creation_date,
                          created_by=quiz.created_by_id)
        self.iterate_questions(quiz.questions, needed.questions)
        return needed

    def add_quiz(self, quiz):
        quiz_uuid = uuid.uuid4()
        new_quiz = Quiz.create(quiz_id=quiz_uuid,
                               quiz_name=quiz.quiz_name,
                               difficult_level=quiz.difficult_level,
                               creation_date=datetime.now(),
                               created_by_id=quiz.created_by)

        for question in quiz.questions:
            new_question = Question.create(question_id=uuid.uuid4(),
                                           question_text=question.question_text,
                                           quiz_id=new_quiz)

            for option in question.options:
                Option.create(option_id=uuid.uuid4(),
                              option_text=option.option_text,
                              is_correct=option.is_correct,
                              question_id=new_question)

        return Quiz.select().where(Quiz.quiz_id == quiz_uuid).get()

    def delete_quiz(self):
        pass

    def check_quiz(self, non_checked_quiz):
        questions = non_checked_quiz.questions

        total_corrects = 0
        for question in questions:
            total_corrects += 1 if sum([i.is_correct for i in question.options if i]) else 0

        total_questions = len(questions)
        return (total_corrects / total_questions) * 100

    def add_quiz_result(self, quiz_result: RequestQuizResult):
        user_quiz_result = UserQuizStatistics.create(
            stat_id=str(uuid.uuid4()),
            accept_rate=quiz_result.accept_percent,
            dispatch_date=quiz_result.dispatch_date,
            user_id=quiz_result.user_id,
            quiz_id=quiz_result.quiz_id
        )
        return user_quiz_result

    def get_user_quiz_statistics(self, user_id: int):
        try:
            stats = (UserQuizStatistics
                     .select(UserQuizStatistics.user_id,
                             User.username,
                             (fn.Sum(UserQuizStatistics.accept_rate) / fn.Count(UserQuizStatistics.stat_id))
                             .alias("rate"))
                     .join(User)
                     .where(UserQuizStatistics.user_id == user_id)
                     .group_by(UserQuizStatistics.user_id, User.user_id)).dicts().get()

            executed_quizzes_dicts = (UserQuizStatistics
                                      .select(Quiz.quiz_id, Quiz.quiz_name, UserQuizStatistics.accept_rate)
                                      .join(Quiz)
                                      .where(UserQuizStatistics.user_id == user_id)).dicts()

            executed_list = [
                ExecutedQuiz(quiz_id=q["quiz_id"],
                             quiz_name=q["quiz_name"],
                             accept_rate=q["accept_rate"]) for q in executed_quizzes_dicts
            ]

            return UserStats(user_id=stats["user_id"],
                             username=stats["username"],
                             average_rating=stats["rate"],
                             executed_quizzes=executed_list)
        except Exception:
            stats = (User
                     .select(User.user_id, User.username)
                     .where(User.user_id == user_id)).dicts().get()

            return UserStats(user_id=stats["user_id"],
                             username=stats["username"],
                             average_rating=0,
                             executed_quizzes=[])

    def iterate_questions(self, questions, storage):
        for question in questions:
            options = [OptionData(i.option_id, i.option_text, i.is_correct) for i in question.options]
            new_question = QuestionData(question.question_id, question.question_text, options)
            storage.append(new_question)
