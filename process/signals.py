"""
Signals for triggering asyn business processes
"""
from django.db.models.signals import pre_save, post_save
from django.utils.module_loading import import_string
from django.dispatch import receiver
from django.conf import settings
from .registry import PROCESS_REGISTRY
from .models import Process, Task
import json

@receiver(post_save, sender=Process, dispatch_uid="process.signals.process_created")
def process_created(sender, instance, created, **kwargs):
    """
    Trigger run when a new appointment process is created
    """
    if created:
        process = PROCESS_REGISTRY.get(instance.process_id)
        for task in process.get('tasks_sync', []):
            task_object = Task.objects.create(process=instance,task_id=task)
            try:
                result = import_string(task)(process)
                task_object.result_data=json.dumps(result)
                task_object.status = 'C'
            except:
                task_object.status = 'F'
            task_object.save()


