from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import NewCalendarForm

# Create your views here.
def home(request):
    return render(request, "Calendar/base.html")


def new_calendar(request):
    if request.method == "GET":
        form = NewCalendarForm()
        context = {"form":form}
        return render(request, "Calendar/new.html", context)
    if request.method == "POST":
        form = NewCalendarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("") # TODO redirect after creating new calendar
        else:
            pass # TODO If form is not correct


