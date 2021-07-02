from .models import Calendar, Task
from django.forms import ModelForm, TextInput, Textarea, DateTimeField, DateField
from django import forms
import datetime


class NewCalendarForm(ModelForm):
    class Meta:
        model = Calendar
        fields = ["name", "description", "author"]
        widgets = {
            "name": TextInput(attrs={"class": "form-control", "placeholder": "Calendar name"}),
            "description": Textarea(attrs={"class": "form-control", "placeholder": "Description"}),
            "author": TextInput(attrs={"class": "form-control", "placeholder": "Your name"})}


class AddTaskForm(forms.Form):
    name = forms.CharField(label='Task title', max_length=63)
    description = forms.CharField(label='Short Description', max_length=255)
    author = forms.CharField(label='Creator', max_length=63)
    date = forms.CharField(widget=forms.TextInput(attrs={"type": "datetime-local"}))

    def save(self, calendar, timezone=None):
        task = Task()
        user_date = datetime.datetime.strptime(self.cleaned_data['date'], "%Y-%m-%dT%H:%M")
        user_date.replace(tzinfo=timezone)
        task.date = user_date
        task.name = self.cleaned_data['name']
        task.description = self.cleaned_data['description']
        try:
            task.author = self.cleaned_data['author']
        except KeyError:
            task.author = ""
        task.timestamp = user_date.timestamp()
        task.year = user_date.year
        task.month = user_date.month
        task.day = user_date.day
        task.calendar = calendar
        task.hour = user_date.hour
        task.minute = user_date.minute
        task.save()
