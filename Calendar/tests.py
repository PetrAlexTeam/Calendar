import datetime

from django.test import TestCase
from .models import Task, Calendar
from .views import get_nearest_month

# Create your tests here.

class ModelsTests(TestCase):
    def setUp(self):
        self.test_cal_name = "Test_calendar"
        self.cal = Calendar.objects.create(name=self.test_cal_name, description="Tester", author="TestClass")
        self.e_task = Task.objects.create(name="Test_task_1", description="Test task 12:00 15 Jan 2021", author="TestClass", timestamp=1610701200, calendar=self.cal)

    def test_create_calendar(self):
        cals = Calendar.objects.filter(name=self.test_cal_name).all()
        self.assertIn(self.cal, cals)

    def test_easy_task_date(self):
        tasks_15_jan = Task.get_day_tasks(date=datetime.date(day=15, month=1, year=2021), calendar=self.cal)
        self.assertIn(self.e_task, tasks_15_jan)

class OtherTests(TestCase):
    def test_get_nearest_month_1(self):
        year, month = 2020, 3
        self.assertEqual(get_nearest_month(year, month), ((2020, 2), (2020, 4)))

    def test_get_nearest_month_2(self):
        year, month = 2020, 1
        self.assertEqual(get_nearest_month(year, month), ((2019, 12), (2020, 2)))

    def test_get_nearest_month_3(self):
        year, month = 2020, 12
        self.assertEqual(get_nearest_month(year, month), ((2020, 11), (2021, 1)))



