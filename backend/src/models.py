from peewee import PostgresqlDatabase, Model, DatabaseProxy
from peewee import CharField, ForeignKeyField, BooleanField, UUIDField, DateTimeField, DoubleField


def setup_database() -> PostgresqlDatabase:
    database_configuration = {
        "database": "quiz_db",
        "user": "postgres",
        "password": "pass",
        "host": "db",
        "port": "5432"
    }

    return PostgresqlDatabase(**database_configuration)


database_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = database_proxy


class User(BaseModel):
    user_id = UUIDField(primary_key=True)
    username = CharField()


class Quiz(BaseModel):
    quiz_id = UUIDField(primary_key=True)
    quiz_name = CharField()
    difficult_level = CharField()
    creation_date = DateTimeField()

    created_by_id = ForeignKeyField(User)


class Question(BaseModel):
    question_id = UUIDField(primary_key=True)
    question_text = CharField()

    quiz_id = ForeignKeyField(Quiz, backref="questions")


class Option(BaseModel):
    option_id = UUIDField(primary_key=True)
    option_text = CharField()
    is_correct = BooleanField()

    question_id = ForeignKeyField(Question, backref="options")


class UserQuizStatistics(BaseModel):
    stat_id = UUIDField(primary_key=True)
    accept_rate = DoubleField()
    dispatch_date = DateTimeField()
    user_id = ForeignKeyField(User)
    quiz_id = ForeignKeyField(Quiz)

    class Meta:
        table_name = "user_stats"


database_proxy.initialize(setup_database())
