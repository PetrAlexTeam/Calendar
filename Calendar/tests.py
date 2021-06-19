import datetime

from django.test import TestCase
from .models import Task, Calendar


# Create your tests here.

class TasksTests(TestCase):
    def setUp(self):
        self.cal = Calendar.objects.create(name="Test_calendar", description="Tester", author="TestClass")
        self.e_task = Task.objects.create(name="Test_task_1", description="Test task 12:00 15 Jan 2021", author="TestClass", timestamp=1610701200, calendar=self.cal)

    def test_easy_date(self):
        tasks_15_jan = Task.get_day_tasks(date=datetime.date(day=15, month=1, year=2021), calendar=self.cal)
        self.assertIn(self.e_task, tasks_15_jan)