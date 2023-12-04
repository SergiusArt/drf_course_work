import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from habits.models import Habit


class HabitTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='user_test@sky.pro', is_superuser=False)
        self.user.set_password('user_test')
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        url = reverse('habits:create')
        data = {
            'user': self.user.id,
            'place': 'Home',
            'time': '12:00',
            'action': 'Exercise',
            'is_pleasant': False,
            'periodicity': 'daily',
            'reward': 'None',
            'execution_time': 60,
            'is_public': False,
            'last_notification': None
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().place, 'Home')

    def test_habit_delete(self):
        habit = Habit.objects.create(user=self.user, place='Home', time='12:00', action='Exercise')
        url = reverse('habits:delete', args=[habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_own_habit_list(self):
        Habit.objects.create(user=self.user, place='Home', time='12:00', action='Exercise')
        Habit.objects.create(user=self.user, place='Gym', time='15:00', action='Workout')
        url = reverse('habits:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.filter(user=self.user).count(), 2)

    def test_public_habit_list(self):
        Habit.objects.create(user=self.user, place='Home', time='12:00', action='Exercise', is_public=True)
        url = reverse('habits:public')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.filter(is_public=True).count(), 1)

    def test_own_habit_retrieve(self):
        habit = Habit.objects.create(user=self.user, place='Home', time='12:00', action='Exercise')
        url = reverse('habits:retrieve', args=[habit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], habit.place)

    def test_own_habit_update(self):
        habit = Habit.objects.create(user=self.user, place='Home', time='12:00', action='Exercise')
        url = reverse('habits:update', args=[habit.id])
        data = {
            'place': 'Gym',
            'time': '15:00',
            'action': 'Workout'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.place, 'Gym')
        self.assertEqual(habit.time.strftime('%H:%M'), '15:00')
        self.assertEqual(habit.action, 'Workout')

    def test_own_habit_partial_update(self):
        habit = Habit.objects.create(user=self.user, place='Home', time='12:00', action='Exercise')
        url = reverse('habits:update', args=[habit.id])
        data = {
            'place': 'Gym'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.place, 'Gym')
        # Получаем текущее время и форматируем его в строку 'HH:MM'
        current_time = datetime.datetime.now().strftime('%H:%M')
        self.assertEqual(habit.time.strftime('%H:%M'), current_time)
        self.assertEqual(habit.action, 'Exercise')
