import os
import requests
from celery import shared_task
from habits.models import Habit
from users.models import User
from datetime import datetime, timedelta


@shared_task
def send_habit_reminder():
    # Получаем список всех пользователей
    users = User.objects.all()
    # Проходимся по всем пользователям
    for user in users:
        # Получаем список всех привычек пользователя
        habits = Habit.objects.filter(user=user)
        # Проходимся по всем привычкам пользователя
        for habit in habits:
            # Получаем время на выполнение привычки
            execution_time = habit.execution_time
            # Получаем время текущего момента
            now = datetime.now()
            # Получаем время начала выполнения привычки
            start_time = habit.time
            # Получаем время окончания выполнения привычки
            end_time = start_time + timedelta(hours=execution_time)
            # Проверяем, является ли текущий момент временем начала выполнения привычки
            if start_time <= now <= end_time:
                # Отправляем сообщение в телеграм бота
                tlg_bot_token = user.telegram_bot_token
                tlg_chat_id = user.telegram_chat_id
                url = f'https://api.telegram.org/bot{tlg_bot_token}/sendMessage'
                msg = f"Напоминание:\n\n - необходимо выполнить привычку '{habit.action}' за время: {execution_time}"
                requests.post(url, data={
                    'chat_id': tlg_chat_id,
                    'text': msg
                })
