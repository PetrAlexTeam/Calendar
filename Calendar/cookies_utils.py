from django.http import HttpResponse

YEARS_3 = 3 * 365 * 24 * 60 * 60  # 3 years


def save_last_calendar(response: HttpResponse, path):
    period = YEARS_3
    response.set_cookie('last_calendar', path, max_age=period)
