from django.db import models
from .registry import PROCESS_REGISTRY

PROCESS_STATUSES = [
    ('N', 'New'),
    ('X', 'Cancelled'),
    ('C', 'Complete'),
    ('F', 'Failed'),
    ('XF', 'Cancelled Failed'),
]

PROCESS_IDS = [(key,key) for key, value in PROCESS_REGISTRY.items()]

class Process(models.Model):
    '''A process combines a number of tasks into a coherant process.
    For example: A new signup process might kick off an array of tasks:
    Now:
    * Create entry in db

    Later:
    * Send a welcome email (now)
    * Send a follow up email tomorrow
    * ... etc
    '''

    def __str__(self):
        return self.name

    process_id = models.CharField(max_length=100, choices=PROCESS_IDS)
    status = models.CharField(max_length=10, choices=PROCESS_STATUSES, default='N')

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    # todo make it hstore
    #should be payload
    request_data = models.TextField(default='{}')


class Task(models.Model):
    '''You should be able to create a task with:

    Task.objects.create_and_run() # create the task and run ummediatate
    Task.objects.create_and_run_later() # create the task and run later
    '''
    process = models.ForeignKey('Process', related_name='tasks', blank=True, null=True)
    task_id = models.CharField(max_length=255)
    input_data = models.TextField(default='{}')
    result_data = models.TextField(default='{}')
    status = models.CharField(max_length=10, choices=PROCESS_STATUSES, default='N')

from .signals import *