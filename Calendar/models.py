from django.contrib.sessions.backends import db
from django.db import models
from random import randint


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
        return f"{self.name} {self.description[:25]}"


class Task(models.Model):
    name = models.CharField(max_length=63, name="name", help_text="Название")
    description = models.TextField(max_length=255, name="description", help_text="Описание")
    creator = models.CharField(max_length=63, name='author', help_text='Автор')
    timestamp = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    hour = models.IntegerField()
    minute = models.IntegerField()
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.description} "
