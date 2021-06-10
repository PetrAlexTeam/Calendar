from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.debug import technical_404_response

from .forms import NewCalendarForm, AddTaskForm2
from .models import Task, Calendar


def home(request):
    context = {"title": "Homepage"}
    return render(request, "Calendar/index.html", context)


def my_calendar(request):
    return render(request, "Calendar/my_calendar.html")


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
        form = AddTaskForm2(request.POST)
        if form.is_valid():
            form.instance.calendar = calendar
            form.save()
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
        form = AddTaskForm2()
        return render(request, "Calendar/add.html", {"form": form, "calendar": calendar})


def get_calendar(request, path):
    """Получение инфо об календаре"""
    try:
        calendar = Calendar.objects.get(path=path)
    except Calendar.DoesNotExist:
        return render(request, "Calendar/404.html", {"text": "calendar not found", "title": "Calendar is not found"})
    tasks = Task.objects.filter(calendar=calendar).all()
    return render(request, "Calendar/calendar.html", {"tasks": tasks})


def support(request):
    context = {"title": "OurContacts"}
    render(request, 'Calendar/support.html', context=context)
