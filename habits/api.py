from rest_framework import generics
from habits.models import Habit
from habits.serializers import HabitSerializer
from users.permissions import IsOwnerPermission
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from users.serializers import UserSerializer


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
    permission_classes = [IsAuthenticated]
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if 'time' in request.data:
            instance.time = request.data['time']
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if 'time' in request.data:
            instance.time = request.data['time']
            instance.save()  # Сохраняем изменения времени выполнения в базе данных
        self.perform_update(serializer)
        return Response(serializer.data)


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


class UserRegistrationView(generics.CreateAPIView):
    """
    API для регистрации нового пользователя.

    Поля:
    - email: почта пользователя (уникальное поле);
    - password: пароль пользователя;
    - tlg_chat_id: Telegram ID пользователя.

    Запросы:
    - POST: Создание нового пользователя. Ожидается передача данных пользователя в формате JSON.
    """

    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
