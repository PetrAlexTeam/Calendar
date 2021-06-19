from .models import Calendar, Task
from django.forms import ModelForm, TextInput, Textarea, DateTimeField, DateField
from django import forms
import datetime
from time import mktime

class NewCalendarForm(ModelForm):
    class Meta:
        model = Calendar
        fields = ["name", "description", "author"]
        widgets = {
            "name": TextInput(attrs={"class": "form-control", "placeholder": "Input calendar.css's name"}),
            "description": Textarea(attrs={"class": "form-control", "placeholder": "Description"}),
            "author": TextInput(attrs={"class": "form-control", "placeholder": "Your name"})}


class AddTaskForm(forms.Form):

    name = forms.CharField(label='Task title', max_length=63)
    description = forms.CharField(label='Short Description', max_length=255)
    author = forms.CharField(label='Creator', max_length=63)
    date = forms.CharField(widget=forms.TextInput(attrs={"type": "datetime-local"}))

    def save(self, calendar):
        print(self.cleaned_data['date'])
        task = Task()
        user_data = datetime.datetime.strptime(self.cleaned_data['date'], "%Y-%m-%dT%H:%M")
        task.date = user_data
        task.name = self.cleaned_data['name']
        task.description = self.cleaned_data['description']
        task.creator = self.cleaned_data['author']
        task.timestamp = user_data.replace(tzinfo=datetime.timezone.utc).timestamp()
        task.year = user_data.year
        task.month = user_data.month
        task.day = user_data.day
        task.calendar = calendar
        task.hour = user_data.hour
        task.minute = user_data.minute
        task.save()
        print(task)
