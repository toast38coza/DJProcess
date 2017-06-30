from django.test import TestCase
from .say_hello import say_hello
class TaskTestCase(TestCase):

    def test_it_prints_hello_world(self):
        say_hello()

    def test_it_returns_a_result(self):
        pass