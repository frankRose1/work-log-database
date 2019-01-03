""" 
  Tests for the functions in main.py
"""
import unittest
import datetime
from unittest.mock import patch

# from peewee import *

import work_log
from validator import Validator
from database_config import Task

MODELS = [Task]

# test_db = SqliteDatabase(':memory:')

test_entry = {
    "title": "Unit testing",
    "date": datetime.datetime.strptime("30/12/2018", '%d/%m/%Y'),
    "employee": "Jane Smith",
    "time_spent": 45,
    "notes": "Some test notes",
}


@patch('builtins.input')
class ValidatorTests(unittest.TestCase):

	def test_validate_date(self, MockInput):
		"""Test that a user can enter a valid date"""
		user_input=['30/12/2018']
		MockInput.side_effect = user_input
		expected_input = Validator.validate_date()
		self.assertEqual(expected_input, test_entry['date'])

	def test_validate_time(self, MockInput):
		"""Test that a user can enter a time duration in minutes"""
		user_input = ['120']
		MockInput.side_effect = user_input
		expected_input = Validator.validate_time()
		self.assertEqual(expected_input, int(user_input[0]))

	def test_validate_employee(self, MockInput):
		"""Test that a user can enter a valid employee name"""
		user_input = [test_entry['employee']]
		MockInput.side_effect = user_input
		expected_input = Validator.validate_employee()
		self.assertEqual(expected_input, test_entry['employee'])

	def test_validate_title(self, MockInput):
		"""Test that a user can enter a valid task title"""
		user_input = [test_entry['title']]
		MockInput.side_effect = user_input
		expected_input = Validator.validate_title()
		self.assertEqual(expected_input, test_entry['title'])

# class AppTests(unittest.TestCase):
#     def setUp(self):
#         test_db.bind(MODELS,bind_refs=False, bind_backrefs=False)
#         test_db.connect()
#         test_db.create_tables(MODELS)

#     def tearDown(self):
#         test_db.drop_tables(MODELS)
#         test_db.close()

if __name__ == '__main__':
    unittest.main()


