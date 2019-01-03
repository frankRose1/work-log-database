import datetime

class Validator:
    """Helper class for checking the users input before it is saved tp the DB"""

    @classmethod
    def validate_employee(cls):
        """Makes sure a value was provided for the employee field"""
        while True:
          employee_name = input('Employee name: ').strip()
          if (len(employee_name) >= 3) and (len(employee_name) <= 200):
            return employee_name
          else:
            print('Error: Please provide an employee name between 3 and 200 characters!')

    @classmethod
    def validate_title(cls):
        """Checks that a value was passed in for task title"""
        while True:
          task_title = input('Title: ').strip()
          if (len(task_title) >= 5) and (len(task_title) <= 200):
            return task_title
          else:
            print('Error: Please provide a title between 5 and 200 characters!')

    @classmethod
    def validate_date(cls):
        """Get task date from the user"""
        while True:
          date_str = input('Task date, use DD/MM/YYYY format: ').strip()
          try:
            date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
            return date
          except ValueError:
            print('Error: {} doesn\'t seem to be a valid date, please try again.'.format(date_str))

    @classmethod
    def validate_time(cls):
        """Gets the time spent on the task from the user"""
        while True:
          time_input = input('Time spent on task (in minutes): ')
          try:
            time_input = int(time_input) 
            return time_input
          except ValueError:
            print('Error: "{}" doesn\'t seem to be a valid time. Numbers only!'.format(time_input))
