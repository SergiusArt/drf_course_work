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

            # Получаем дату и время последнего оповещения привычки
            last_note = habit.last_notification

            # Получаем время текущего момента
            now = datetime.now().replace(second=0, microsecond=0)

            # Получаем время начала выполнения привычки
            start_time = habit.time.replace(second=0, microsecond=0)

            # Проверяем периодичность перед отправкой оповещения
            if habit.periodicity == 'daily':
                # Проверяем, было ли последнее оповещение выполнено сегодня или раньше и если время начала выполнения
                # привычки равно текущему времени
                if (last_note is None or last_note.date() < now.date()) and start_time == now:
                    send_notification.delay(habit, execution_time)
            elif habit.periodicity == 'weekly':
                # Проверяем, было ли последнее оповещение выполнено на прошлой неделе или раньше и если время начала
                # выполнения привычки равно текущему времени
                if (last_note is None or last_note.date() < (now - timedelta(days=7)).date()) and start_time == now:
                    send_notification.delay(habit, execution_time)


@shared_task
def send_notification(habit, execution_time):
    # Отправляем сообщение в телеграм бота
    tlg_bot_token = os.getenv('TLG_BOT_TOKEN')
    tlg_chat_id = habit.user.tlg_chat_id
    url = f'https://api.telegram.org/bot{tlg_bot_token}/sendMessage'
    msg = f"Напоминание:\n\n - необходимо выполнить привычку '{habit.action}' за: {execution_time} секунд."
    requests.post(url, data={
        'chat_id': tlg_chat_id,
        'text': msg
    })

    # Обновляем поле last_notification текущей привычки
    habit.last_notification = datetime.now()
    habit.save()
