from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Team, Activity, Leaderboard, Workout
from django.contrib.auth import get_user_model

User = get_user_model()

class APITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_api_root(self):
        response = self.client.get(reverse('api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)

    def test_team_list(self):
        Team.objects.create(name='Marvel')
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Marvel')

    def test_workout_list(self):
        Workout.objects.create(name='Pushups', description='Do 20 pushups', difficulty='Easy')
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Pushups')
