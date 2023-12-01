from rest_framework.generics import ListAPIView
from .models import Habit
from .serializers import HabitSerializer


class PublicHabitListView(ListAPIView):
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
