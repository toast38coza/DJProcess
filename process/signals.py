"""
Signals for triggering asyn business processes
"""
from django.db.models.signals import post_save
from django.utils.module_loading import import_string
from django.dispatch import receiver
from .registry import PROCESS_REGISTRY
from .models import Process, Task
import json, yaml

def validate_payload(self, data, payload_definition):
    pass

def extract_arguments(self, data, expected_payload):
    pass

def execute_tasks(instance, tasks, async=False):

    if async:
        print ('not yet implemented')

    for task in tasks:
        task_name = task.get('task')
        task_object = Task.objects.create(
                        process=instance,
                        task_id=task_name)

        try:
            data = json.loads(instance.request_data)
            result = import_string(task_name)(**data)
            task_object.result_data=json.dumps(result)
            task_object.status = 'C'
        except:
            task_object.status = 'F'
            # put the error message on the result_data
        task_object.save()


@receiver(post_save, sender=Process, dispatch_uid="process.signals.process_created")
def process_created(sender, instance, created, **kwargs):
    """
    Trigger run when a new appointment process is created
    """
    if created:
        process_file = PROCESS_REGISTRY.get(instance.process_id)
        process_path = './process/processes/{}.yml'.format(process_file)
        process_data = {}
        with open(process_path) as f:
            process_content = f.read()
            process_data = yaml.safe_load(process_content)

        tasks_now = process_data.get('tasks', [])
        execute_tasks(instance, tasks_now)

        async_tasks_now = process_data.get('tasks_async', [])
        execute_tasks(instance, async_tasks_now, async=True)

        # schedule tasks:



