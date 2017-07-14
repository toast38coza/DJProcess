from django.test import TestCase, Client
from django.urls import reverse

from ..models import Task, Process
from ..signals import extract_arguments

class RegistryAPIEndpointTestCase(TestCase):

    def test_api(self):
        url = reverse('registry_tasks-list')
        c = Client()
        response = c.get(url)
        assert response.status_code == 200

"""
class ExtractArgumentsTestCase(TestCase):

    def test_can_get_argument_from_payload(self):
        payload_data = {
            'message': 'test',
            'foo': 'bar'
        }
        args_def = {
            'key': 'message'
        }
        expected_result: {
            'message': 'test'
        }
        extract_arguments(data, required_args)
"""

class CreateProcessAPIEndpointTestCase(TestCase):

    def setUp(self):
        self.url = reverse('process-list')
        data = {
            'process_id': 'hello-world',
            "message": "Hello!"
        }
        self.client = Client()
        self.result = self.client.post(self.url, data)

    def test_is_ok(self):
        assert self.result.status_code == 201

    def test_it_creates_a_process(self):
        assert Process.objects.count() == 1

    def test_process_id_can_be_specified_as_a_GET_param(self):
        url = '{}?process_id={}'.format(reverse('process-list'), 'hello-world')
        data = {
            'request_data': '{"message": "Hello!"}'
        }
        result = self.client.post(url, data)
        assert result.status_code == 201


    def test_it_creates_a_task(self):
        num_tasks = Task.objects.count()
        assert num_tasks == 1,\
            'Expect 1 task to exist. Got: {}'.format(num_tasks)

    def test_it_executes_the_task(self):
        task = Task.objects.first()
        assert task.status == 'C',\
            'Expected status: C. Got: {}'.format(task.status)

    def test_it_stores_the_response_as_json(self):
        task = Task.objects.first()
        assert task.result_data == '{"result": "Hello!"}'
