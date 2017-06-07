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

    def __str__(self):
        return self.name

    process_id = models.CharField(max_length=100, choices=PROCESS_IDS)
    status = models.CharField(max_length=10, choices=PROCESS_STATUSES, default='N')

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    # todo make it hstore
    request_data = models.TextField(default='{}')


class Task(models.Model):
    process = models.ForeignKey('Process', related_name='tasks')
    task_id = models.CharField(max_length=255)
    input_data = models.TextField(default='{}')
    result_data = models.TextField(default='{}')
    status = models.CharField(max_length=10, choices=PROCESS_STATUSES, default='N')

from .signals import *