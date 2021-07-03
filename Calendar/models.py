from django.contrib.sessions.backends import db
from django.db import models
from random import randint
from datetime import datetime
import datetime as dt
from django.shortcuts import get_object_or_404
from django.core.exceptions import FieldError


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
    author = models.CharField(max_length=63, name='author', help_text='Автор')
    path = models.CharField(max_length=63, name='path', help_text='Путь по которому получают этот календарь',
                            unique=True)

    def __str__(self):
        return f"{self.name} {self.description[:25]} {self.author}"

    def __repr__(self):
        return str(self)


class Task(models.Model):
    @staticmethod
    def get_day_tasks(date, calendar: Calendar) -> list:
        """Returns list of task by day
        :param date datetime.date object
        :param calendar models.Calendar object in which we trying to find tasks
        :returns list[models.Task]
        """
        if type(date) != dt.date:
            date = date.date()
        return list(Task.objects.filter(date_time__date=date, calendar=calendar).order_by(
            "timestamp"))

    @staticmethod
    def delete_task(task_id: int, calendar_path: str):
        cal = get_object_or_404(Calendar, path=calendar_path)
        task = get_object_or_404(Task, id=task_id, calendar=cal)
        task.delete()  # TODO Каскадное даление для повторяющихся задач

    @staticmethod
    def update(task_id: int, calendar_path: str, **kwargs):
        cal = get_object_or_404(Calendar, path=calendar_path)
        task = get_object_or_404(Task, id=task_id, calendar=cal)
        for field_name, value in kwargs.items():
            setattr(task, field_name, value)
        task.save()
        return task

    def save(self, *args, **kwargs):
        if self.timestamp is None:
            self.timestamp = self.date_time.timestamp()
        if self.author == "":
            self.author = self.calendar.author
        if self.date_time is None:
            self.date_time = datetime.fromtimestamp(self.timestamp)
        return super().save(*args, **kwargs)

    name = models.CharField(max_length=63, name="name", help_text="Название")
    description = models.TextField(max_length=255, name="description", help_text="Описание")
    timestamp = models.IntegerField()

    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    author = models.CharField(max_length=63, name='author', help_text='Автор', default="Anonymous")
    date_time = models.DateTimeField(name="date_time")

    def __str__(self):
        return f"{self.name} {self.description} {self.author} {self.timestamp} {self.date_time}"

    def __repr__(self):
        return str(self)

    def get_json(self):
        return {"name": self.name,
                "description": self.description,
                "datetime": self.date_time,
                "author": self.author,
                "calendar_id": self.calendar_id}

