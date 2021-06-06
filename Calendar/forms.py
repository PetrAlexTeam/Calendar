from .models import Calendar, Task
from django.forms import ModelForm, TextInput, Textarea, DateTimeField, DateField
from django import forms


class NewCalendarForm(ModelForm):
    class Meta:
        model = Calendar
        fields = ["name", "description", "author"]
        widgets = {
            "name": TextInput(attrs={"class": "form-control", "placeholder": "Input calendar's name"}),
            "description": Textarea(attrs={"class": "form-control", "placeholder": "Description"}),
            "author": TextInput(attrs={"class": "form-control", "placeholder": "Your name"})}


class AddTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "author", "timestamp"]
        widgets = {
            "name": TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
            "description": Textarea(attrs={"class": "form-control", "placeholder": "Description"}),
            "author": TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
            "timestamp": TextInput()
        }
