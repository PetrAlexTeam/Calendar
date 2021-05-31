from .models import Calendar
from django.forms import ModelForm, TextInput, Textarea


class NewCalendarForm(ModelForm):
    class Meta:
        model = Calendar
        fields = ["name", "description", "author"]
        widgets = {
            "name":         TextInput(attrs={"class": "form-control", "placeholder": "Input calendar's name"}),
            "description":  Textarea(attrs={"class": "form-control", "placeholder": "Description"}),
            "author":       TextInput(attrs={"class": "form-control", "placeholder": "Your name"})}
