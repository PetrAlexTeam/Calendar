from django.db import models
from random import randint
from datetime import datetime, timedelta
import datetime as dt
from django.shortcuts import get_object_or_404
from django.db import transaction

TEN_YEARS = datetime(year=20, month=1, day=1) - datetime(year=10, month=1, day=1)


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


class RepeatedTaskManager(models.Manager):
    def create_repeated_tasks(self, base_task, period, end_date=None):
        """New repeated task
        :param base_task - abstrac Task
        :param period - timedelta object. How often should task be repeated
        :param end_date - datetime until which tasks will be repeated or it will be repeated for 10 years
        """
        end_date = end_date or base_task.date_time + TEN_YEARS
        date = base_task.date_time + period
        with transaction.atomic():
            while date <= end_date:
                base_task.clone_task(date)
                date += period


class Task(models.Model):
    name = models.CharField(max_length=63, name="name", help_text="Название")
    description = models.TextField(max_length=255, name="description", help_text="Описание", default="No description")
    timestamp = models.IntegerField(null=True)

    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    author = models.CharField(max_length=63, name='author',
                              help_text='Автор',
                              default="Anonymous")
    date_time = models.DateTimeField(name="date_time", null=True)
    inherited = models.ForeignKey("self",
                                  verbose_name="Базовая задача в случае если это задача - повторяющаяся",
                                  null=True, on_delete=models.CASCADE)
    abstract_task = models.BooleanField(verbose_name="Является ли это абстрактной задачей для какой то повторяющейся",
                                        default=False)
    repeated = RepeatedTaskManager()

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

    def clone_task(self, date_time):
        """Create Task with the same name, desc, etc but at other dt. It will be inherited to self"""
        t = Task(name=self.name,
                 description=self.description,
                 author=self.author,
                 date_time=date_time,
                 inherited=self)
        return t

    def save(self, *args, **kwargs):
        if self.timestamp is None:
            self.timestamp = self.date_time.timestamp()
        if self.author == "":
            self.author = self.calendar.author
        if self.date_time is None:
            self.date_time = datetime.fromtimestamp(self.timestamp)
        return super().save(*args, **kwargs)

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
