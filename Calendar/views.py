from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.debug import technical_404_response
import calendar
from .forms import NewCalendarForm, AddTaskForm
from .models import Task, Calendar


def home(request):
    context = {"title": "Homepage"}
    return render(request, "Calendar/index.html", context)


def my_calendar(request):
    c = calendar.Calendar()
    context = {"date": c.monthdatescalendar(2021, 1)}
    print(context["date"])
    return render(request, "Calendar/my_calendar.html", context)


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
            return redirect(f"/{path}")
        else:
            error = 'Problems with this calendar. Try again.'
            context = {"error": error}
            return render(request, 'Calendar/new.html', context)


def add_task(request, path):
    if request.method == 'POST':
        print("Get post")
        try:
            calendar = Calendar.objects.get(path=path)
        except Calendar.DoesNotExist:
            print(404)
            return render(request, "Calendar/404.html",
                          {"text": "calendar not found", "title": "Calendar is not found"})
        form = AddTaskForm(request.POST)
        if form.is_valid():
            print("save is coming")
            form.save(calendar = calendar)
            return redirect(f"/{calendar.path}")
        else:
            error = 'Problems with this task. Try again.'
            context = {"error": error}
            return render(request, 'Calendar/add.html', context)

    elif request.method == 'GET':
        try:
            calendar = Calendar.objects.get(path=path)
        except Calendar.DoesNotExist:
            return render(request, "Calendar/404.html",
                          {"text": "calendar not found", "title": "Calendar is not found"})
        form = AddTaskForm()
        return render(request, "Calendar/add.html", {"form": form, "calendar": calendar})


def get_calendar(request, path):
    """Получение инфо об календаре"""
    try:
        calendar = Calendar.objects.get(path=path)
    except Calendar.DoesNotExist:
        return render(request, "Calendar/404.html", {"text": "calendar not found", "title": "Calendar is not found"})
    tasks = Task.objects.filter(calendar=calendar).order_by("timestamp")
    # print(type(calendar))
    print(str(calendar))
    # links = calendar + "add"
    # print(links)
    return render(request, "Calendar/calendar.html", {"tasks": tasks, "calendar": calendar})


def support(request):
    context = {"title": "OurContacts"}
    render(request, 'Calendar/support.html', context=context)
