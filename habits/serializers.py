from rest_framework import serializers
from habits.models import Habit


# Сериализатор привычек
class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        if data.get('linked_habit') and data.get('reward'):
            raise serializers.ValidationError('Нельзя одновременно указывать связанную привычку и вознаграждение')
        execution_time = data.get('execution_time')
        if execution_time is not None and execution_time > 120:
            raise serializers.ValidationError('Время выполнения не может быть больше 120 секунд')

        if data.get('linked_habit') and not data.get('linked_habit').is_pleasant:
            raise serializers.ValidationError(
                'В связанные привычки могут попадать только привычки с признаком приятной')
        if data.get('is_pleasant') and (data.get('reward') or data.get('linked_habit')):
            raise serializers.ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки')

        return data
