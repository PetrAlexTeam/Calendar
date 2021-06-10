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
            "timestamp": TextInput(attrs={"class": "form-control", "placeholder": "datetime", "type": "date"}),
            "date": TextInput(attrs={"class": "form-control", "placeholder": "datetime", "type": "date"})
        }

class AddTaskForm2(forms.Form):
    name = forms.CharField(label='Task title', max_length=63)
    description = forms.CharField(label='Short Description', max_length=255)
    author = forms.CharField(label='Creator', max_length=63, default='Anonymous')
    date = forms.DateTimeField()
