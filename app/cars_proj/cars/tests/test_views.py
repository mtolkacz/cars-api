from django.test import TestCase
from django.urls import reverse

from ..models import Make, Car


class CarAPITests(TestCase):

    def setUp(self):
        m = Make.objects.get_or_create(
            make_id=1,
            make_name='TestMake'
        )
        Car.objects.get_or_create(
            model_id=1,
            model_name='TestModel',
            make=m
        )
        self.create_read_url = reverse('cars:list_create_update')

    def test_list(self):
        response = self.client.get(self.create_read_url)

        self.assertContains(response, 'TestMake')
        self.assertContains(response, 'TestModel')
