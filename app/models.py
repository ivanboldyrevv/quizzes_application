from peewee import PostgresqlDatabase, Model
from peewee import CharField, ForeignKeyField, BooleanField, UUIDField


db = PostgresqlDatabase("quiz_db", user="postgres", password="pass", host="db", port="5432")


class BaseModel(Model):
    class Meta:
        database = db


class Quiz(BaseModel):
    quiz_id = UUIDField(primary_key=True)
    quizname = CharField()


class Question(BaseModel):
    question_id = UUIDField(primary_key=True)
    question_text = CharField()

    quiz_id = ForeignKeyField(Quiz, backref="questions")


class Option(BaseModel):
    option_id = UUIDField(primary_key=True)
    option_name = CharField()
    is_correct = BooleanField()

    question_id = ForeignKeyField(Question, backref="options")
