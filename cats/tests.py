import json

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from .models import SpyCat




class SpyCatAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.spy_cat1 = SpyCat.objects.create(name='Whiskers', years_of_experience=5, breed='Siamese', salary=1000)
        self.spy_cat2 = SpyCat.objects.create(name='Felix', years_of_experience=2, breed='Maine Coon', salary=800)


    def post_request(self, url, payload, expected_status_code=200):
        return self.client.post(url, data=json.dumps(payload), content_type='application/json')

    def put_request(self, url, payload, expected_status_code=200):
        return self.client.put(url, data=json.dumps(payload), content_type='application/json')

    def delete_request(self, url):
        return self.client.delete(url)

    def patch_request(self, url, payload, expected_status_code=200):
        return self.client.patch(url, data=json.dumps(payload), content_type='application/json')

    def test_list_spy_cats(self):
        response = self.client.get("/api/spy_cats/")
        self.assertEqual(response.status_code, 200)
        spy_cats = response.json().get('items', [])
        self.assertIn('Whiskers', [cat['name'] for cat in spy_cats])
        self.assertEqual(len(spy_cats), 2)

    def test_get_spy_cat(self):
        response = self.client.get(f"/api/spy_cats/{self.spy_cat1.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Whiskers')

    def test_create_spy_cat(self):
        payload = {'name': 'Tom', 'years_of_experience': 3, 'breed': 'Persian', 'salary': 1200}
        response = self.post_request("/api/spy_cats/", payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Tom')
        self.assertEqual(response.json()['salary'], 1200)

    def test_create_spy_cat_name_empty(self):
        payload = {'name': '', 'years_of_experience': 3, 'breed': 'Persian', 'salary': 1200}
        response = self.post_request("/api/spy_cats/", payload)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()['detail'][0]['msg'], 'Value error, Name must not be empty')

    def test_create_spy_cat_negative_years_of_experience(self):
        payload = {'name': 'Tom', 'years_of_experience': -1, 'breed': 'Persian', 'salary': 1200}
        response = self.post_request("/api/spy_cats/", payload)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()['detail'][0]['msg'], 'Value error, Years of experience must be a positive number')

    def test_create_spy_cat_invalid_breed(self):
        payload = {'name': 'Tom', 'years_of_experience': 3, 'breed': 'UnknownBreed', 'salary': 1200}
        response = self.post_request("/api/spy_cats/", payload)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()['detail'][0]['msg'], "Value error, UnknownBreed is not a valid breed")

    def test_create_spy_cat_negative_salary(self):
        payload = {'name': 'Tom', 'years_of_experience': 3, 'breed': 'Persian', 'salary': -1200}
        response = self.post_request("/api/spy_cats/", payload)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()['detail'][0]['msg'], 'Value error, Salary must be a positive number')

    def test_update_spy_cat(self):
        payload = {'name': 'Updated Tom', 'years_of_experience': 4, 'breed': 'Persian', 'salary': 1300}
        response = self.put_request(f"/api/spy_cats/{self.spy_cat1.id}/", payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Updated Tom')
        self.assertEqual(response.json()['salary'], 1300)

    def test_update_spy_cat_salary(self):
        payload = {'salary': 1500}
        response = self.patch_request(f"/api/spy_cats/{self.spy_cat1.id}/salary", payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['salary'], 1500)

    def test_update_spy_cat_salary_invalid(self):
        payload = {'salary': -500}
        response = self.patch_request(f"/api/spy_cats/{self.spy_cat1.id}/salary", payload)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()['detail'][0]['msg'], 'Value error, Salary must be a positive number')

    def test_delete_spy_cat(self):
        response = self.delete_request(f"/api/spy_cats/{self.spy_cat1.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertFalse(SpyCat.objects.filter(id=self.spy_cat1.id).exists())

