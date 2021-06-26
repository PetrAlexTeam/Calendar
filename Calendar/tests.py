import datetime

from django.conf.urls import url
from django.test import TestCase

from .forms import NewCalendarForm, AddTaskForm
from .models import Task, Calendar
from .views import get_nearest_month


# Create your tests here.

class ModelsTests(TestCase):
    def setUp(self):
        self.test_cal_name = "Test_calendar"
        self.cal = Calendar.objects.create(name=self.test_cal_name, description="Tester", author="TestClass")
        self.e_task = Task.objects.create(name="Test_task_1", description="Test task 12:00 15 Jan 2021",
                                          author="TestClass", timestamp=1610701200, calendar=self.cal)

    def test_create_calendar(self):
        cals = Calendar.objects.filter(name=self.test_cal_name).all()
        self.assertIn(self.cal, cals)

    def test_easy_task_date(self):
        tasks_15_jan = Task.get_day_tasks(date=datetime.date(day=15, month=1, year=2021), calendar=self.cal)
        self.assertIn(self.e_task, tasks_15_jan)


class NewTaskFormTest(TestCase):
    def setUp(self):
        self.test_cal_name = "Test_calendar"
        self.cal = Calendar.objects.create(name=self.test_cal_name, description="Tester", author="TestClass")

    def test_create_new_task(self):
        form_data = {"name": "AutoTestCal12331",
                     "description": "I am created by Robo",
                     "author": "tests.py",
                     "date": "2020-11-10T15:45"}
        form = AddTaskForm(data=form_data)
        form.is_valid()
        form.save(self.cal)
        self.assertEqual(len(Task.objects.filter(name=form_data["name"], calendar=self.cal).all()), 1)
        self.assertEqual(Task.objects.get(name=form_data["name"], calendar=self.cal).author, form_data["author"])
        self.assertEqual(Task.objects.get(name=form_data["name"], calendar=self.cal).year, 2020)
        self.assertEqual(Task.objects.get(name=form_data["name"], calendar=self.cal).hour, 15)

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
