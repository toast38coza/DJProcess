from django.core.management.base import BaseCommand
import os

task_content = """

def {}(*args, **kwargs):
    '''...'''
    pass
"""

test_task_content = """
from django.test import TestCase
from .{} import {}
class TaskTestCase(TestCase):

    def test_it_does_{}(self):
        pass
"""

init_content = """
'''
Module description goes here ..
---

## Commands:

* Run the tests: `web python manage.py test process.tasks.{}`
'''
from .{} import {}
"""

class Command(BaseCommand):
    help = 'Generate a task'

    def add_arguments(self, parser):
        '''Params: practitioner_id'''
        parser.add_argument('module')
        parser.add_argument('task')

    def handle(self, *args, **options):
        print(options)
        module = options.get('module')
        task = options.get('task')
        path = './process/tasks/{}'.format(module)
        files = [
            ('{}/__init__.py'.format(path), init_content.format(module, task, task)),
            ('{}/{}.py'.format(path, task), task_content.format(task)),
            ('{}/test_{}.py'.format(path, task), test_task_content.format(task, task, task)),
        ]
        os.makedirs(path, exist_ok=True)
        for file, content in files:
            if not os.path.exists(file):
                f = open(file, 'w')
                f.write(content)
                f.close()
                print ('* Created: {}'.format(file))
            else:
                print('* {} already exists. I\'m not going to make any changes'.format(file))

        print('---------------')
        print('TODO:')
        print('1. If this is a new module, you will need to register your module (`process.tasks.{}`) in: `process/registry.py`'.format(module))
        print('2. You may need to add an import for your task in: `process/tasks/{}/__init__.py`'.format(module))

