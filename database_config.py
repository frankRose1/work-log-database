"""
  Set up the database and models
"""
from peewee import *

db = SqliteDatabase('worklog.db')

class Task(Model):
    employee= CharField(max_length=150)
    title = CharField(max_length=200)
    time_spent = IntegerField()
    date = DateField()
    notes = TextField(null=True)

    class Meta:
        database = db


def initialize_db():
    """Connect to the database and create the tables"""
    db.connect()
    db.create_tables([Task], safe=True)