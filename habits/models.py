from django.db import models

from config import settings
from src.constants import NULLABLE


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        **NULLABLE)
    place = models.CharField(max_length=255, verbose_name='Место', **NULLABLE)
    time = models.TimeField(auto_now_add=True, verbose_name='Время')
    action = models.CharField(max_length=255, verbose_name='Действие', **NULLABLE)
    is_pleasant = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    linked_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Связанная привычка', **NULLABLE)
    periodicity = models.CharField(
        max_length=20,
        choices=(('daily', 'Ежедневно'), ('weekly', 'Еженедельно'),),
        default='daily',
        verbose_name='Периодичность'
    )
    reward = models.CharField(max_length=255, verbose_name='Вознаграждение', **NULLABLE)
    execution_time = models.IntegerField(verbose_name='Время на выполнение', **NULLABLE)
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')
    # дата и время последнего оповещения привычки
    last_notification = models.DateTimeField(**NULLABLE, verbose_name='Дата и время последнего оповещения')

    def __str__(self):
        return self.action
