from django.contrib.sessions.backends import db
from django.db import models
from random import randint
from datetime import datetime


class Calendar(models.Model):
    @staticmethod
    def generate_path() -> str:
        return str(randint(10 ** 6, 9 * 10 ** 6))

    def save(self, *args, **kwargs):
        if not self.path:
            self.path = self.generate_path()
        return super().save(*args, **kwargs)

    name = models.CharField(max_length=63, name="name", help_text="Название")
    description = models.TextField(max_length=255, name="description", help_text="Описание")
    creator = models.CharField(max_length=63, name='author', help_text='Автор')
    path = models.CharField(max_length=63, name='path', help_text='Путь по которому получают этот календарь',
                            unique=True)

    def __str__(self):
        return f"{self.name} {self.description[:25]} "


class Task(models.Model):
    @staticmethod
    def get_day_tasks(date: datetime.date, calendar: Calendar) -> list:
        return list(Task.objects.filter(day=date.day, month=date.month, year=date.year, calendar=calendar).order_by("timestamp"))


    def save(self, *args, **kwargs):
        print(self.day)
        if True:
            print(type(self.timestamp))
            dt = datetime.fromtimestamp(self.timestamp)
            self.year = dt.year
            self.month = dt.month
            self.day = dt.day
            self.hour = dt.hour
            self.minute = dt.minute
        return super().save(*args, **kwargs)

    name = models.CharField(max_length=63, name="name", help_text="Название")
    description = models.TextField(max_length=255, name="description", help_text="Описание")
    timestamp = models.IntegerField()
    # Для более быстрой работы базы данных и удобного вывода помимо таймстампа можно сохранять и месяц день итп.
    # Количество памяти занимаемой БД не так критично как время загрзи страницы

    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    hour = models.IntegerField()
    minute = models.IntegerField()
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    creator = models.CharField(max_length=63, name='author', help_text='Автор', default="Anonymous")

    def __str__(self):
        return f"{self.name} {self.description} {self.timestamp}"
