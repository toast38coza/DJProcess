from django.test import TestCase
from ..models import Process, Task
from ..signals import extract_arguments, recursive_lookup
import json

class ProcessSignalTestCase(TestCase):

    def setUp(self):
        payload = '{"message": "testing"}'
        self.process = Process.objects.create(
                        process_id='hello-world',
                        request_data=payload)
        self.tasks = Task.objects.filter(process_id=self.process.id)

    def test_process_creates_tasks(self):
        assert len(self.tasks) == 1

    def test_task_executes(self):
        task = self.tasks.first()
        result = json.loads(task.result_data).get('result')
        assert result == 'testing', \
            'Expected result to be testing. got: {}'.format(result)

'''
    def test_creates_correct_task(self):
        assert self.tasks[0].task_id == 'process.tasks.io.say_hello'

    def test_updates_task_status(self):
        assert self.tasks[0].status == 'C',\
            'Expected task to complete successfull. Result was: {}'.format(self.tasks[0].__dict__)
'''

class RecursiveLookupTestCase(TestCase):

    def setUp(self):
        self.data = {'payload': {'foo': {'bar': {'baz': 'bus'}}}}

    def test_nested_lookup(self):
        key = 'payload.foo.bar.baz'
        result = recursive_lookup(key, self.data)
        assert result == 'bus', 'Expected bus. Got: {}'.format(result)

    def test_base_lookup(self):
        key = 'payload'
        result = recursive_lookup(key, self.data)
        assert result == self.data.get('payload'), \
            'Got: {}'.format(result)

    def test_middle_lookup(self):
        key = 'payload.foo.bar'
        result = recursive_lookup(key, self.data)
        assert result == {'baz': 'bus'}, \
            'Expected {\'baz\': \'bus\'}. Got: {}'.format(result)

    def test_incorrect_key_throws_keyerror(self):
        key = 'key.does.not.exist'
        with self.assertRaises(Exception) as context:
            recursive_lookup(key, self.data)

    def test_can_specify_default(self):
        key = 'key.does.not.exist'
        result = recursive_lookup(key, self.data, 'default')
        assert result == 'default'

class ExtractArgsTestCase(TestCase):

    def test_simple_non_nested_argument(self):
        payload = { 'message': 'testing' }
        payload_definition = {'message': 'payload.message'}

        result = extract_arguments(payload, payload_definition)
        assert result['message'] == 'testing', \
            'Expected foo to be bar. Actual response: {}'.format(result)
        assert result.get('baz', None) is None

    def test_passing_the_whole_payload(self):
        pass

    def test_passing_nested_argument(self):
        pass
