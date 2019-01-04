""" 
	Unit tests for the application
	Tests are included for Search, Validator, and work_log
"""
import unittest
import datetime
from unittest.mock import patch, Mock

from peewee import *

import work_log
from search import Search
from validator import Validator
from database_config import Task

MODELS = [Task]

test_db = SqliteDatabase(':memory:')

test_entry_1 = {
    "title": "Unit testing",
    "date": datetime.datetime.strptime("30/12/2018", '%d/%m/%Y'),
    "employee": "Jane Smith",
    "time_spent": 45,
    "notes": "Some test notes",
}

test_entry_2 = {
    "title": "Search class tests",
    "date": datetime.datetime.strptime("01/01/2019", '%d/%m/%Y'),
    "employee": "John Smith",
    "time_spent": 45,
    "notes": "Making sure the search class has coverage",
}


@patch('builtins.input')
class ValidatorTests(unittest.TestCase):

		def test_validate_date(self, MockInput):
				"""Test that a user can enter a valid date"""
				user_input=['30/12/2018']
				MockInput.side_effect = user_input
				expected_input = Validator.validate_date()
				self.assertEqual(expected_input, test_entry_1['date'])

		def test_validate_time(self, MockInput):
				"""Test that a user can enter a time duration in minutes"""
				user_input = ['120']
				MockInput.side_effect = user_input
				expected_input = Validator.validate_time()
				self.assertEqual(expected_input, int(user_input[0]))

		def test_validate_employee(self, MockInput):
				"""Test that a user can enter a valid employee name"""
				user_input = [test_entry_1['employee']]
				MockInput.side_effect = user_input
				expected_input = Validator.validate_employee()
				self.assertEqual(expected_input, test_entry_1['employee'])

		def test_validate_title(self, MockInput):
				"""Test that a user can enter a valid task title"""
				user_input = [test_entry_1['title']]
				MockInput.side_effect = user_input
				expected_input = Validator.validate_title()
				self.assertEqual(expected_input, test_entry_1['title'])

class BaseTestCase(unittest.TestCase):
		"""To be used on any tests that require the database being set up"""
		def setUp(self):
				test_db.bind(MODELS,bind_refs=False, bind_backrefs=False)
				test_db.connect()
				test_db.create_tables(MODELS)
				self.task_1 = test_entry_1
				self.task_2 = test_entry_2
				self.add_test_tasks(self.task_1)
				self.add_test_tasks(self.task_2)
			
		def tearDown(self):
				test_db.drop_tables(MODELS)
				test_db.close()

		def add_test_tasks(self, test_task):
				with patch('builtins.input', side_effect=['y']):
						work_log.create_task(test_task)


@patch('builtins.input')
class SearchTests(BaseTestCase):

		def test_search_by_time(self, MockInput):
				"""Two results should be returned that match 45 minutes"""
				user_input = [45]
				MockInput.side_effect = user_input
				expected_output = Search.by_time()
				self.assertEqual(len(expected_output), 2)

		def test_search_by_employee(self, MockInput):
				"""Should be one entry found for the employee John"""
				MockInput.side_effect = ['john']
				expected_output = Search.by_name()
				self.assertEqual(len(expected_output), 1)
				self.assertEqual(expected_output[0].employee, self.task_2['employee'])

		def test_search_by_date(self, MockInput):
				"""Should show one result for 30/12/2018"""
				MockInput.side_effect = ['30/12/2018']
				expected_output = Search.by_date()
				self.assertEqual(len(expected_output), 1)
				self.assertIsInstance(expected_output[0].employee, str)

		def test_search_by_term(self, MockInput):
				"""Should return 2 search results for the term "test" """
				MockInput.side_effect = ['test']
				expected_output = Search.by_term()
				self.assertEqual(len(expected_output), 2)
				self.assertIn('test', expected_output[0].title)
				self.assertIn('test', expected_output[1].title)

class WorkLogTests(BaseTestCase):

		def test_delete_task(self):
				"""After being deleted, search result for "John" should be 0"""
				with patch('builtins.input', side_effect=['john', 'y', 'john']):
						with patch('builtins.print') as mock_print:
								# should find one match for "john"
								employee_match = Search.by_name()
								self.assertEqual(len(employee_match), 1)
								# delete the task
								work_log.delete_task(employee_match[0])
								# length should now be zero
								expected_output = Search.by_name()
								self.assertEqual(len(expected_output), 0)
								mock_print.assert_called_once_with('Task was deleted!')

		def test_get_task_data(self):
				"""Get task data should gather input from the user and return a dict"""
				user_inputs = ['Dave Chapelle', 'Writing unit tests', 30, '03/01/2019',
											'some random notes']
				with patch('builtins.input', side_effect=user_inputs):
						expected_output = work_log.get_task_data()
						self.assertIsInstance(expected_output, dict)
						self.assertEqual(expected_output['employee'], user_inputs[0])
						self.assertEqual(expected_output['time_spent'], user_inputs[2])

		@patch('builtins.input', side_effect=['q'])
		@patch('work_log.quit_program')
		def test_quit_program(self, mock_input, mock_quit_program):
				"""Quit program should be called if user types "q" """
				work_log.print_main_menu()
				mock_quit_program.assert_called_once()

if __name__ == '__main__':
    unittest.main()


