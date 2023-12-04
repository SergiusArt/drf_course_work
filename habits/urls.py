from django.urls import path
from habits.apps import HabitsConfig
from .api import HabitList, PublicHabitList, HabitCreate, HabitRetrieveAPIView, HabitUpdateAPIView, HabitDestroyAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('', HabitList.as_view(), name='list'),
    path('public/', PublicHabitList.as_view(), name='public'),
    path('create/', HabitCreate.as_view(), name='create'),
    path('<int:pk>/', HabitRetrieveAPIView.as_view(), name='retrieve'),
    path('<int:pk>/update/', HabitUpdateAPIView.as_view(), name='update'),
    path('<int:pk>/delete/', HabitDestroyAPIView.as_view(), name='delete'),
]
