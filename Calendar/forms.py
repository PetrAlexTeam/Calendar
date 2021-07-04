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
    description = forms.CharField(label='Short Description', max_length=255, required=False)
    author = forms.CharField(label='Creator', max_length=63, required=False)
    date = forms.CharField(widget=forms.TextInput(attrs={"type": "datetime-local"}))
    CHOICES = [(None, "No repeat"), (1, "Every day"), (7, "Every week")]
    repeat_at = forms.ChoiceField(widget=forms.RadioSelect, label="repeat task", choices=CHOICES, required=False)

    def save(self, calendar, timezone=None):
        from_date = datetime.datetime.strptime(self.cleaned_data['date'], "%Y-%m-%dT%H:%M")
        from_date.replace(tzinfo=timezone)

        task = Task()
        task.name = self.cleaned_data['name']
        task.description = self.cleaned_data['description']
        try:
            task.author = self.cleaned_data['author']
        except KeyError:
            task.author = ""
        task.calendar = calendar
        if self.cleaned_data.get("repeat_at"):
            task.abstract_task = True
            task.save()
            period = datetime.timedelta(days=int(self.cleaned_data["repeat_at"]))
            Task.repeated.create_repeated_tasks(task, period, start_date=from_date)
        else:
            # If task is not repeating
            task.date = from_date
            task.timestamp = from_date.timestamp()
            task.save()

