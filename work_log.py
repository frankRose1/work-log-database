"""
    Work Log Database

    Terminal application that uses an Sqlite database and allows users to create a task by entering 
    their name, task title, amount of time and any general notes regarding the task. Can also search 
    tasks and view a report in the terminal.
"""
import os
from collections import OrderedDict

from search import Search
from validator import Validator
from database_config import initialize_db, Task

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def view_tasks(tasks):
    """Cycle through any tasks found and allow user to edit/delete a task
    Arguments:
        :tasks: list of tasks found
    """
    if len(tasks) >= 1:
        results = len(tasks)
        counter = 1
        for task in tasks:
            clear_terminal()
            print('='*20)
            print('Employee: {}'.format(task.employee))
            print('Title: {}'.format(task.title))
            print('Date (YYYY/MM/DD): {}'.format(task.date))
            print('Time Spent (in minutes): {}'.format(task.time_spent))
            if task.notes:
                print('Notes: {}'.format(task.notes))
            print('\nResult {} of {}\n'.format(counter, results))
            print('='*20)
            print('[N]ext, [E]dit, [D]elete [R]eturn to menu')
            next_action = input('Action: [Nedr] ').strip().lower()

            if next_action == 'r':
                break
            elif next_action == 'd':
                delete_task(task)
            elif next_action == 'e':
                edit_task(task)
            counter += 1
    else:
        clear_terminal()
        input('No results found. Press enter to return to search menu ')

def get_task_data():
    """Gets the task data from the user"""
    employee_name = Validator.validate_employee()
    task_title = Validator.validate_title()
    task_time = Validator.validate_time()
    task_date = Validator.validate_date()
    task_notes = input('Notes (optional): ').strip()
    return {
        'employee': employee_name,
        'title': task_title,
        'time_spent': task_time,
        'date': task_date,
        'notes': task_notes
    }

def create_task(new_task):
    """Create a new task entry"""
    if input('Save entry? [Yn] ').lower().strip() != 'n':
        Task.create(employee=new_task['employee'], title=new_task['title'], 
                    time_spent=new_task['time_spent'], date=new_task['date'], 
                    notes=new_task['notes'])
        return True

def delete_task(task):
    """Deletes a task from the Database"""
    if input('Are you sure you want to delete this entry? [yN] ').lower().strip() == 'y':
        task.delete_instance()
        print('Task was deleted!')

def edit_task(task):
    """Updates/saves a task"""
    updated_task = get_task_data()
    if input('Update entry? [Yn] ').lower().strip() != 'n':
        task.employee = updated_task['employee']
        task.title = updated_task['title']
        task.time_spent = updated_task['time_spent']
        task.date = updated_task['date']
        task.notes = updated_task['notes']
        task.save()
        print('Task updated!')

def quit_program():
    """Quit program"""
    print('\nUser has ended the program.')


search_menu = OrderedDict([
    ('a', Search.by_name),
    ('b', Search.by_date),
    ('c', Search.by_time),
    ('d', Search.by_term)
])

def print_search_menu():
    """Search tasks"""
    search_choice = None
    while search_choice != 'q':
        clear_terminal()
        print('Enter "q" to return to main menu')
        for key, value in search_menu.items():
            print('{}) {}'.format(key, value.__doc__))

        search_choice = input('Your choice: ').lower().strip()
        if search_choice in search_menu:
            tasks = search_menu[search_choice]()
            view_tasks(tasks)

main_menu = OrderedDict([
    ('a', create_task),
    ('s', print_search_menu),
    ('q', quit_program)
])

def print_main_menu():
    """Print a menu of options for the user"""
    user_choice = None
    while user_choice != 'q':
        clear_terminal()
        print('WORK LOG DATABASE')
        print('='*17)
        for key, value in main_menu.items():
            print('{}) {}'.format(key, value.__doc__))
        user_choice = input('Your choice: ').lower().strip()
        if user_choice in main_menu:
            if user_choice == 'a':
                new_task = get_task_data()
                if main_menu[user_choice](new_task):
                    print('Entry added')
            else:
                main_menu[user_choice]()

if __name__ == '__main__':
    """Initialize the db and print the menu"""
    initialize_db()
    print_main_menu()
