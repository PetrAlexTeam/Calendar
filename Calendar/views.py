from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.debug import technical_404_response

from .forms import NewCalendarForm
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
        form.instance.path = Calendar.generate_path()
        if form.is_valid():
            form.save()
            path = form.instance.path
            return redirect(f"/{path}")
        else:
            error = 'Problems with this calendar. Try again.'
            context = {"error": error}
            return render(request, 'Calendar/new.html', context)


def get_calendar(request, path):
    """Получение инфо об календаре"""
    try:
        calendar = Calendar.objects.get(path=path)
    except Calendar.DoesNotExist:
        return render(request, "Calendar/404.html", {"text": "такого календаря нет", "title": "Calendar is not found"})
    tasks = Task.objects.filter(calendar=calendar).all()
    print(calendar, tasks)
    return render(request, "Calendar/calendar.html", {"tasks": tasks})


def add_task(request, path):
    pass


def support(request):
    context = {'title': 'Our Contacts'}
    render(request, 'Calendar/support.html', context)
