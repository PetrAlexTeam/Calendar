from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index', views.home, name='home'),
    path('new', views.new_calendar, name='new_calendar'),
    path('my_calendar', views.my_calendar, name='month_calendar'),
    path('tasks/<str:path>', views.get_calendar),
    path('<str:path>/add', views.add_task),
    path('<str:path>/<int:year>/<int:month>', views.my_calendar),
    path('<str:path>', views.current_month_calendar, name="calendar"),
    path('support', views.support, name='support')
]
