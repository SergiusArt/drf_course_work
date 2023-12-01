from rest_framework import generics
from habits.models import Habit
from habits.serializers import HabitSerializer
from users.permissions import IsOwnerPermission
from rest_framework.permissions import IsAuthenticated


# API для списка и создания привычек пользователя
class HabitList(generics.ListAPIView):
    """
    API для получения списка привычек пользователя.

    Разрешения:
    - Аутентифицированные пользователи могут видеть только свои привычки.

    Поля:
    - user: пользователь;
    - place: место привычки;
    - time: время;
    - action: действие;
    - is_pleasant: признак приятной привычки;
    - linked_habit: связанная привычка;
    - periodicity: периодичность;
    - reward: вознаграждение;
    - execution_time: время на выполнение;
    - is_public: признак публичности;

    Запросы:
    - GET: Получение списка привычек пользователя.
    """

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerPermission]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


# API для списка публичных привычек
class PublicHabitList(generics.ListAPIView):
    """
    API для получения списка публичных привычек.

    Разрешения:
    - Не требуется аутентификация для просмотра списка привычек.

    Поля:
    - user: пользователь;
    - place: место привычки;
    - time: время;
    - action: действие;
    - is_pleasant: признак приятной привычки;
    - linked_habit: связанная привычка;
    - periodicity: периодичность;
    - reward: вознаграждение;
    - execution_time: время на выполнение;
    - is_public: признак публичности;

    Запросы:
    - GET: Получение списка публичных привычек.
    """
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer


# API для создания привычки
class HabitCreate(generics.CreateAPIView):
    """
    API для создания привычки.

    Разрешения:
    - Аутентифицированные пользователи могут создавать привычки.

    Поля:
    - user: пользователь;
    - place: место привычки;
    - time: время;
    - action: действие;
    - is_pleasant: признак приятной привычки;
    - linked_habit: связанная привычка;
    - periodicity: периодичность;
    - reward: вознаграждение;
    - execution_time: время на выполнение;
    - is_public: признак публичности;

    Запросы:
    - POST: Создание новой привычки.
    """
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    API для получения информации о конкретной привычке.

    Разрешения:
    - Аутентифицированные пользователи могут просматривать только свою привычку.

    Поля:
    - user: пользователь;
    - place: место привычки;
    - time: время;
    - action: действие;
    - is_pleasant: признак приятной привычки;
    - linked_habit: связанная привычка;
    - periodicity: периодичность;
    - reward: вознаграждение;
    - execution_time: время на выполнение;
    - is_public: признак публичности;

    Запросы:
    - GET: Получение информации о конкретной привычке.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerPermission]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """
    API для обновления информации о конкретной привычке.

    Разрешения:
    - Аутентифицированные пользователи могут обновлять только свою привычку.

    Поля:
    - user: пользователь;
    - place: место привычки;
    - time: время;
    - action: действие;
    - is_pleasant: признак приятной привычки;
    - linked_habit: связанная привычка;
    - periodicity: периодичность;
    - reward: вознаграждение;
    - execution_time: время на выполнение;
    - is_public: признак публичности;

    Запросы:
    - PUT: Обновление информации о привычке.
    - PATCH: Частичное обновление информации о конкретной привычке
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerPermission]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """
    API для удаления конкретной привычки.

    Разрешения:
    - Аутентифицированные пользователи могут удалять только свою привычку.

    Поля:
    - user: пользователь;
    - place: место привычки;
    - time: время;
    - action: действие;
    - is_pleasant: признак приятной привычки;
    - linked_habit: связанная привычка;
    - periodicity: периодичность;
    - reward: вознаграждение;
    - execution_time: время на выполнение;
    - is_public: признак публичности;

    Запросы:
    - DELETE: Удаление конкретной привычки.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerPermission]
