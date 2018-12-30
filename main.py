"""
    Work Log Database

    Terminal application that uses an SQlite database and allows users to create a task by entering 
    their name, task title, amount of time and any general notes regarding the task. Can also search 
    tasks and view a report in the terminal.
"""
import datetime
from collections import OrderedDict

from peewee import *

db = SqliteDatabase('worklog.db')

class BaseClass(Model):
    class Meta:
        database = db

class Task(BaseClass):
    worker_name = None
    title = None
    date = None
    notes = None


def initialize_db():
    """Connect to the database and create the tables"""
    db.connect()
    db.create_tables([Task], safe=True)

def print_menu():
    """Print a menu of options for the user"""
    pass

if __name__ == '__main__':
    """Initialise the db and print the menu"""
    initialize_db()
    print_menu()
