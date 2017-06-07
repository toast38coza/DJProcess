from django.test import TestCase
from ..models import Process, Task

class ProcessSignalTestCase(TestCase):

    def setUp(self):
        self.process = Process.objects.create(process_id='hello-world')
        self.tasks = Task.objects.filter(process_id=self.process.id)

    def test_process_creates_tasks(self):
        assert len(self.tasks) == 1

    def test_creates_correct_task(self):
        assert self.tasks[0].task_id == 'process.tasks.say_hello'

    def test_updates_task_status(self):
        assert self.tasks[0].status == 'C'