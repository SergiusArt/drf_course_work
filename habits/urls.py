from django.urls import path
from habits.apps import HabitsConfig
from .api import *

app_name = HabitsConfig.name

urlpatterns = [
    path('habits/', HabitList.as_view()),
    path('habits/public/', PublicHabitList.as_view()),
    path('habits/create/', HabitCreate.as_view()),
    path('habits/<int:pk>/', HabitRetrieveAPIView.as_view()),
    path('habits/<int:pk>/update/', HabitUpdateAPIView.as_view()),
    path('habits/<int:pk>/delete/', HabitDestroyAPIView.as_view()),
]