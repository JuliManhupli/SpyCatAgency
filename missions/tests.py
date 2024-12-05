import json
from django.test import TestCase, Client
from .models import Mission, Target
from cats.models import SpyCat


class MissionAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.spy_cat1 = SpyCat.objects.create(name='Whiskers', years_of_experience=5, breed='Siamese', salary=1000)
        self.spy_cat2 = SpyCat.objects.create(name='Felix', years_of_experience=2, breed='Maine Coon', salary=800)
        self.mission1 = Mission.objects.create(
            name='Mission 1',
            description='Test Mission 1',
            assigned_cat=self.spy_cat1,
            is_completed=False
        )
        self.target1 = Target.objects.create(
            mission=self.mission1,
            name='Target 1',
            country='Ukraine',
            notes='Test Target 1',
            is_completed=False
        )

    def post_request(self, url, payload, expected_status_code=200):
        return self.client.post(url, data=json.dumps(payload), content_type='application/json')

    def patch_request(self, url, payload, expected_status_code=200):
        return self.client.patch(url, data=json.dumps(payload), content_type='application/json')

    def delete_request(self, url):
        return self.client.delete(url)

    def test_list_missions(self):
        response = self.client.get("/api/missions/")
        self.assertEqual(response.status_code, 200)
        missions = response.json().get('items', [])
        self.assertIn('Mission 1', [mission['name'] for mission in missions])
        self.assertEqual(len(missions), 1)

    def test_create_mission(self):
        payload = {
            'name': 'Mission 2',
            'description': 'Test Mission 2',
            'assigned_cat': self.spy_cat2.id,
            'targets': [
                {'name': 'Target 2', 'country': 'USA', 'notes': 'Test Target 2'}
            ]
        }
        response = self.post_request("/api/missions/", payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Mission 2')
        self.assertEqual(response.json()['assigned_cat']['id'], self.spy_cat2.id)

    def test_assign_cat_to_mission(self):
        payload = {}
        response = self.patch_request(f"/api/missions/{self.mission1.id}/assign-cat/{self.spy_cat2.id}/", payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['assigned_cat']['id'], self.spy_cat2.id)

    def test_remove_cat_from_mission(self):
        payload = {}
        response = self.patch_request(f"/api/missions/{self.mission1.id}/remove-cat/", payload)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()['assigned_cat'])

    def test_mark_target_as_completed(self):
        payload = {}
        response = self.patch_request(f"/api/missions/{self.mission1.id}/target/{self.target1.id}/complete/", payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['is_completed'])

    def test_delete_mission(self):
        self.mission1.assigned_cat = None
        self.mission1.save()
        response = self.delete_request(f"/api/missions/{self.mission1.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertFalse(Mission.objects.filter(id=self.mission1.id).exists())

    def test_create_mission_with_invalid_cat(self):
        payload = {
            'name': 'Mission Invalid Cat',
            'description': 'Test Invalid Cat Mission',
            'assigned_cat': 9999,
            'targets': [
                {'name': 'Target 1', 'country': 'Ukraine', 'notes': 'Test Target 1'}
            ]
        }
        response = self.post_request("/api/missions/", payload, expected_status_code=400)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Spy cat with ID 9999 not found.', response.json()['detail'])

    def test_create_mission_with_no_targets(self):
        payload = {
            'name': 'Mission Without Targets',
            'description': 'Mission without any targets',
            'assigned_cat': self.spy_cat1.id,
            'targets': []
        }
        response = self.post_request("/api/missions/", payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Mission Without Targets')
        self.assertEqual(len(response.json()['targets']), 0)


    def test_delete_mission_with_assigned_cat(self):
        payload = {}
        response = self.delete_request(f"/api/missions/{self.mission1.id}/")
        self.assertEqual(response.status_code, 400)
        self.assertIn('Cannot delete mission assigned to a cat.', response.json()['detail'])

