from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new', views.new_calendar, name='new_calendar'),
    path('<str:path>', views.get_calendar),
    path('<str:path>/add', views.add_task),
    path('support', views.support, name='support')
]
