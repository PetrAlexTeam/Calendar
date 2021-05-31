from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import NewCalendarForm


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
            return redirect('home')  # TODO redirect after creating new calendar
        else:
            error = 'task was unsuccesfully'
            context = {"error": error}
            return render(request, 'Calendar/new.html', context)
            # TODO If form is not correct
