from django.contrib.sessions.backends import db
from django.db import models


class Calendar(models.Model):
    name = models.CharField(max_length=63, name="name", help_text="Название")
    description = models.TextField(max_length=255, name="description", help_text="Описание")
    creator = models.CharField(max_length=63, name='author', help_text='Автор')


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

