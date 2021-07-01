import calendar as calendar_engine
from datetime import datetime

from models import Calendar, Task
from collections import namedtuple

Calendar_data = namedtuple("Calendar_data", "month_string_weeks tasks days")


def get_nearest_month(year, month):
    """Returns tuple of tuples: ((y_prev, m_prev), (y_next, m_next))"""
    if month == 12:
        next_ = (year + 1, 1)
        previous = (year, 11)
    elif month == 1:
        next_ = (year, 2)
        previous = (year - 1, 12)
    else:
        next_ = (year, month + 1)
        previous = (year, month - 1)
    return previous, next_


def generate_calendar_data(month: int, year: int, calendar: Calendar):
    c = calendar_engine.Calendar()
    tasks = {}
    days = {}
    month_string_weeks = []
    for weak in c.monthdatescalendar(year, month):
        week = []
        for date in weak:
            data_els = date.ctime().split()  # data elements: day, month, year etc.
            str_date = data_els[1] + ' ' + data_els[2] + ', ' + data_els[4]
            week.append(str_date)
            days[str_date] = data_els[2]  # Save day number only
            tasks[str_date] = Task.get_day_tasks(date, calendar)
        month_string_weeks.append(week)
    calendar_data = Calendar_data(month_string_weeks=month_string_weeks, tasks=tasks, days=days)
    return calendar_data


def get_month_name(month: int):
    return datetime.strptime(str(month), "%m").strftime("%b")