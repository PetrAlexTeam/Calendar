import json

from django.shortcuts import render, redirect, get_object_or_404
from .calendar_utils import get_nearest_month, generate_calendar_data, get_month_name
from .cookies_utils import save_last_calendar
from .forms import NewCalendarForm, AddTaskForm
from .models import Task, Calendar
from datetime import datetime
import calendar as calendar_engine
from django.core.exceptions import FieldError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def home(request):
    context = {"title": "Homepage"}
    return render(request, "Calendar/index.html", context)


def show_calendar(request, path, year, month):
    c = calendar_engine.Calendar()

    calendar = get_object_or_404(Calendar, path=path)

    calendar_data = generate_calendar_data(month, year, calendar)
    tasks = calendar_data.tasks
    month_string_weeks = calendar_data.month_string_weeks
    days = calendar_data.days

    previous, next_ = get_nearest_month(year, month)
    previous_link = f"/{path}/{previous[0]}/{previous[1]}"  # TODO Переделать через urls
    next_link = f"/{path}/{next_[0]}/{next_[1]}"

    today_tasks = Task.get_day_tasks(datetime.now(), calendar)
    decoding_month = {'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 'Apr': 'April', 'May': 'May', 'Jun': 'June',
                      'Jul': 'July', 'Aug': 'August', 'Sep': 'September', 'Oct': 'October', 'Nov': 'November',
                      'Dec': 'December'}
    current_month = decoding_month[get_month_name(month)]
    context = {"month": c.monthdatescalendar(year, month),
               "tasks": tasks, "month_string": month_string_weeks,
               "next_link": next_link,
               "previous_link": previous_link,
               "calendar": calendar,
               "today_tasks": today_tasks,
               "current_month": current_month,
               "days": days,

               }
    resp = render(request, "Calendar/my_calendar.html", context)
    save_last_calendar(resp, path)
    return resp


def new_calendar(request):
    """ Слздание новго каленадря /new"""
    if request.method == "GET":
        form = NewCalendarForm()
        context = {"form": form}
        return render(request, "Calendar/new.html", context)
    if request.method == "POST":
        form = NewCalendarForm(request.POST)
        if form.is_valid():
            form.save()
            path = form.instance.path
            month = datetime.now().month
            year = datetime.now().year
            return redirect(f"/{path}/{year}/{month}")  # TODO Переделать в джиджу
        else:
            error = 'Problems with this calendar. Try again.'
            context = {"error": error}
            return render(request, 'Calendar/new.html', context)


def add_task(request, path):
    if request.method == 'POST':
        calendar = get_object_or_404(Calendar, path=path)
        form = AddTaskForm(request.POST)
        if form.is_valid():
            form.save(calendar=calendar, timezone=None)
            return redirect(f"/{calendar.path}")  # TODO переделать в шаблонизаторе
        else:
            error = 'Problems with this task. Try again.'
            context = {"error": error}
            return render(request, 'Calendar/add.html', context)

    elif request.method == 'GET':
        calendar = get_object_or_404(Calendar, path=path)
        form = AddTaskForm()
        return render(request, "Calendar/add.html", {"form": form, "calendar": calendar})


def get_calendar(request, path):
    """Получение инфо об календаре"""
    calendar = get_object_or_404(Calendar, path=path)
    tasks = Task.objects.filter(calendar=calendar).order_by("timestamp")
    return render(request, "Calendar/tasks.html", {"tasks": tasks, "calendar": calendar})


def support(request):
    context = {"title": "OurContacts"}
    render(request, 'Calendar/support.html', context=context)


def current_month_calendar(request, path):
    year, month = datetime.today().year, datetime.today().month
    return redirect(f"/{path}/{year}/{month}")


def last(request):
    """Get last opened calendar by user"""
    if request.COOKIES.get('last_calendar'):
        return redirect(f"/{request.COOKIES.get('last_calendar')}")
    else:
        return redirect("/new")


def get_task(request, path, task_id):
    """Open task [ID: task_id] page"""
    calendar = get_object_or_404(Calendar, path=path)
    task = get_object_or_404(Task, id=task_id, calendar=calendar)
    task_day = task.get_day_tasks(task.date_time.date(),
                                  calendar)  # TODO Переименовать в day_tasks, в том числе в шаблонизватор
    context = {"task": task,
               "calendar": calendar,
               "task_day": task_day}
    return render(request, "Calendar/task.html", context=context)


# API to Update and Edit Tasks
@csrf_exempt  # We don't need csrf validation in this form now, but # TODO enable csrf protection
def update_task(request, path: str, task_id: int):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        task = Task.update(task_id, path, **data)
        return JsonResponse(task.get_json())


@csrf_exempt  # We don't need csrf validation in this form now, but # TODO enable csrf protection
def delete_task(request, path: str, task_id: int):
    if request.method == "POST":
        Task.delete_task(calendar_path=path, task_id=task_id)
        return JsonResponse({"OK": "Success"})
