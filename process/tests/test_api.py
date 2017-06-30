from django.test import TestCase, Client
from django.urls import reverse


class RegistryAPIEndpointTestCase(TestCase):

    def test_api(self):
        url = reverse('registry_tasks-list')
        c = Client()
        response = c.get(url)
        assert response.status_code == 200