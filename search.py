from database_config import Task
from validator import Validator

class Search:
	"""Provides various methods for searching for tasks"""

	@classmethod
	def by_name(cls):
		"""Search by employee name"""
		name_query = input('Employee name: ')
		tasks = (Task
				.select()
				.where(Task.employee.contains(name_query))
				.order_by(Task.date.desc()))
		return tasks

	@classmethod
	def by_date(cls):
		"""Search by date"""
		date_query = Validator.validate_date()
		tasks = (Task
				.select()
				.where(Task.date == date_query)
				.order_by(Task.date.desc()))
		return tasks

	@classmethod
	def by_time(cls):
		"""Search by time spent on task"""
		time_query = Validator.validate_time()
		tasks = (Task
				.select()
				.where(Task.time_spent == time_query)
				.order_by(Task.date.desc()))
		return tasks

	@classmethod
	def by_term(cls):
		"""Search by a term in either title or notes"""
		term_query = input('Enter your search term: ').strip()
		tasks = (Task
				.select()
				.where(
					(Task.title.contains(term_query)) | 
					(Task.notes.contains(term_query)))
					.order_by(Task.date.desc()))
		return tasks