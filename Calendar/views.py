from django.shortcuts import render, redirect
import calendar as calendar_engine

from .calendar_utils import get_nearest_month
from .cookies_utils import save_last_calendar
from .forms import NewCalendarForm, AddTaskForm
from .models import Task, Calendar
from datetime import datetime
from django.db.models import ObjectDoesNotExist


def home(request):
    context = {"title": "Homepage"}
    return render(request, "Calendar/index.html", context)


def show_calendar(request, path, year, month):
    try:
        calendar = Calendar.objects.get(path=path)
    except Calendar.DoesNotExist:
        return render(request, "Calendar/404.html", {"text": "calendar not found", "title": "Calendar is not found"})
    c = calendar_engine.Calendar()
    tasks = {}
    days = {}
    month_string = []
    for weak in c.monthdatescalendar(year, month):
        week = []
        for date in weak:
            data_els = date.ctime().split()
            str_date = data_els[1] + ' ' + data_els[2] + ', ' + data_els[4]
            week.append(str_date)
            days[str_date] = data_els[2]  # Save day number only
            tasks[str_date] = Task.get_day_tasks(date, calendar)
        month_string.append(week)

    previous, next_ = get_nearest_month(year, month)
    previous_link = f"/{path}/{previous[0]}/{previous[1]}"
    next_link = f"/{path}/{next_[0]}/{next_[1]}"

    today_task = Task.get_day_tasks(datetime.now(), calendar)
    current_month = datetime.strptime(str(month), "%m").strftime("%b")
    context = {"month": c.monthdatescalendar(year, month),
               "tasks": tasks, "month_string": month_string,
               "next_link": next_link,
               "previous_link": previous_link,
               "calendar": calendar,
               "today_task": today_task,
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
        try:
            my_calendar = Calendar.objects.get(path=path)
        except Calendar.DoesNotExist:
            return render(request, "Calendar/404.html",
                          {"text": "calendar not found", "title": "Calendar is not found"})
        form = AddTaskForm(request.POST)
        if form.is_valid():
            form.save(calendar=my_calendar)
            return redirect(f"/{my_calendar.path}")
        else:
            error = 'Problems with this task. Try again.'
            context = {"error": error}
            return render(request, 'Calendar/add.html', context)

    elif request.method == 'GET':
        try:
            my_calendar = Calendar.objects.get(path=path)
        except Calendar.DoesNotExist:
            return render(request, "Calendar/404.html",
                          {"text": "calendar not found", "title": "Calendar is not found"})
        form = AddTaskForm()
        return render(request, "Calendar/add.html", {"form": form, "calendar": my_calendar})


def get_calendar(request, path):
    """Получение инфо об календаре"""
    try:
        calendar = Calendar.objects.get(path=path)
    except Calendar.DoesNotExist:
        return render(request, "Calendar/404.html", {"text": "calendar not found", "title": "Calendar is not found"})
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
    try:
        calendar = Calendar.objects.get(path=path)
        task = Task.objects.get(id=task_id, calendar=calendar)
    except ObjectDoesNotExist:
        return render(request,
                      "Calendar/404.html",
                      {"text": "Something going wrong", "title": "Something going wrong"})
    date = datetime(task.year, task.month, task.day)
    task_day = task.get_day_tasks(date, calendar)
    context = {"task": task,
               "calendar": calendar,
               "task_day": task_day}
    return render(request, "Calendar/task.html", context=context)
