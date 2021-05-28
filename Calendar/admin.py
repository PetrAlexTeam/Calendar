from django.contrib import admin
from .models import Calendar, Task

admin.site.register(Task)
admin.site.register(Calendar)
# Register your models here.
