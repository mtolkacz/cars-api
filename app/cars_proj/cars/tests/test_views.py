import base64

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from ..models import Make, Car, Rate


class CarAPITests(TestCase):

    def setUp(self):
        username = 'john'
        password = 'glass onion'
        self.user = User.objects.create_user(
                        username=username,
                        email='jlennon@beatles.com',
                        password=password,
                    )
        self.make = Make.objects.create(
            make_id=1,
            make_name='TestMake'
        )
        self.car = Car.objects.create(
            model_id=1,
            model_name='TestModel',
            make=self.make,
        )
        self.rated_car = Car.objects.create(
            model_id=2,
            model_name='RatedModel',
            make=self.make,
        )
        self.rate = Rate.objects.get_or_create(
            car=self.car,
            user=self.user,
            rate=1,
        )

        # Add default basic authentication to every request
        login_data = f'{username}:{password}'
        credentials = base64.b64encode(bytes(login_data, encoding='utf8')).decode('utf8')
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + credentials

    def test_create_update(self):
        self.url = reverse('cars:list_create_update')
        post = {
            'make': 'Fiat',
            'model': '500',
        }
        response = self.client.post(self.url, post)
        self.assertIn(response.status_code, [200, 201])
        self.assertEqual(Car.objects.count(), 3)

    def test_list(self):
        self.url = reverse('cars:list_create_update')
        response = self.client.get(self.url)
        self.assertContains(response, self.car.make.make_name)
        self.assertContains(response, self.car.model_name)

    def test_popular(self):
        self.url = reverse('cars:popular_list')
        response = self.client.get(self.url)
        self.assertContains(response, self.car.make.make_name)

    def test_rate(self):
        self.url = reverse('cars:rate')
        post = {
            'pk': str(self.rated_car.pk),
            'rate': '5',
        }
        response = self.client.post(self.url, post)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rate.objects.count(), 2)
