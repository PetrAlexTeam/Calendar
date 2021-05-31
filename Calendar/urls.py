from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('new', views.new_calendar),
    path('<str:path>', views.get_calendar),
]
