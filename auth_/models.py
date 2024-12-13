from peewee import Model
from peewee import CharField, UUIDField
from peewee import PostgresqlDatabase


db = PostgresqlDatabase("auth-dev-db", user="auth-dev", password="pass", host="auth-service-database", port="5432")
db.connect()


class User(Model):
    uid = UUIDField(primary_key=True)
    username = CharField()
    password = CharField()

    class Meta:
        database = db
