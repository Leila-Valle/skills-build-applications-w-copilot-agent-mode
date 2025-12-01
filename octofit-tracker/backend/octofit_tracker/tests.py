from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from .models import Team, Activity, Workout

User = get_user_model()

class BasicModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass')
        self.team = Team.objects.create(name='Team A')
        self.activity = Activity.objects.create(name='Running', metric='km')

    def test_workout_creation(self):
        w = Workout.objects.create(user=self.user, activity=self.activity, value=5.0, units='km')
        self.assertEqual(w.user.username, 'tester')

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_api_root(self):
        url = reverse('api_root')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
