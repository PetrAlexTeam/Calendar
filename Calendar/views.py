from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.debug import technical_404_response

from .forms import NewCalendarForm, AddTaskForm
from .models import Task, Calendar


def home(request):
    return render(request, "Calendar/page.html")


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
        try:
            calendar = Calendar.objects.get(path=path)
        except Calendar.DoesNotExist:
            return render(request, "Calendar/404.html",
                          {"text": "calendar not found", "title": "Calendar is not found"})
        form = AddTaskForm(request.POST)
        if form.is_valid():
            print(type(form.instance))
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
        form = AddTaskForm()
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
    context = {'title': 'Our Contacts'}
    render(request, 'Calendar/support.html', context)
