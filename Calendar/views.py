from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import NewCalendarForm
from .models import Task, Calendar

def home(request):
    return render(request, "Calendar/base.html")



def new_calendar(request):
    """ Слздание новго каленадря /new"""
    if request.method == "GET":
        form = NewCalendarForm()
        context = {"form": form}
        return render(request, "Calendar/new.html", context)
    if request.method == "POST":
        error = ''
        form = NewCalendarForm(request.POST)
        if form.is_valid():
            form.save()
            path = form.instance.path
            return redirect(f"/{path}")
        else:
            error = 'task was unsuccesfully'
            context = {"error": error}
            # /<calendar_path>
            return render(request, 'Calendar/new.html', context)


def get_calendar(request, path):
    """Получение инфо об календаре"""
    calendar = Calendar.objects.filter(path=path).first()
    tasks = Task.objects.filter(calendar=calendar).all()
    return render(request, "Calendar/calendar.html", {"tasks": tasks})


def support(request):
    render(request, 'Calendar/support.html')
