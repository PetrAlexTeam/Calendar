from django.http import HttpResponse


def save_last_calendar(response: HttpResponse, path):
    one_year = 365 * 24 * 60 * 60
    response.set_cookie('last_calendar', path, max_age=one_year)