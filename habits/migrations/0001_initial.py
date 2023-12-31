# Generated by Django 4.2.7 on 2023-11-30 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(blank=True, max_length=255, null=True, verbose_name='Место')),
                ('time', models.TimeField(auto_now_add=True, verbose_name='Время')),
                ('action', models.CharField(blank=True, max_length=255, null=True, verbose_name='Действие')),
                ('is_pleasant', models.BooleanField(default=False, verbose_name='Признак приятной привычки')),
                ('periodicity', models.IntegerField(default=1, verbose_name='Периодичность')),
                ('reward', models.CharField(blank=True, max_length=255, null=True, verbose_name='Вознаграждение')),
                ('execution_time', models.IntegerField(blank=True, null=True, verbose_name='Время на выполнение')),
                ('is_public', models.BooleanField(default=False, verbose_name='Признак публичности')),
                ('linked_habit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='habits.habit', verbose_name='Связанная привычка')),
            ],
        ),
    ]
