from typing import List, Any
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class OptionData:
    option_id: str
    option_name: str
    is_correct: bool


@dataclass
class QuestionData:
    question_id: str
    question_text: str
    option: List[OptionData] = field(default_factory=list)


@dataclass
class QuizData:
    quiz_id: str
    quiz_name: str
    difficult_level: str
    creation_date: datetime
    created_by: str
    questions: List[Any] = field(default_factory=list)


@dataclass
class ExecutedQuiz:
    quiz_id: str
    quiz_name: str
    accept_rate: float


@dataclass
class UserStats:
    user_id: str
    username: str
    average_rating: float
    executed_quizzes: List[ExecutedQuiz]
