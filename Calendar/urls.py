from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index', views.home, name='index'),
    path('new', views.new_calendar, name='new_calendar'),
    path('support', views.support, name='support'),
    path("last", views.last, name="last_calendar"),
    path("<str:path>/tasks/<int:task_id>", views.get_task, name="task"),
    path('<str:path>/tasks', views.get_calendar, name="calendar_tasks"),
    path('<str:path>/add', views.add_task, name="add_task"),
    path('<str:path>/<int:year>/<int:month>', views.show_calendar, name="month_calendar"),
    path('<str:path>', views.current_month_calendar, name="current_month_calendar"),
    url(r'^tz_detect/', include('tz_detect.urls'))
]
