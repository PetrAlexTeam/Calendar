from datetime import datetime, timedelta
from functools import partial
from random import randint
from tqdm import tqdm
from faker import Faker
from django.core.management.base import BaseCommand
from Calendar.models import Calendar, Task

rand_100 = partial(randint, 1, 100)
f = Faker()


def create_calendar_if_not_eisit(path, options):
    if Calendar.objects.filter(path=path).all():
        if options["verbosity"] >= 2:
            print(f"Find already exist calendar [path: {path}]")
        calendar = Calendar.objects.get(path=path)
    else:
        if options["verbosity"] >= 2:
            print(f"Created new calendar [path: {path}]")
        calendar = Calendar.objects.create(path=path,
                                           name="Test Calendar",
                                           description="This calendar created automatically for manual testing",
                                           author="generator.py")
    return calendar


class Command(BaseCommand):
    help = "Generate test calendar"

    def handle(self, *args, **options):
        start_date = datetime.strptime(options["start"], "%Y-%m-%dT%H:%M")
        end_date = datetime.strptime(options["end"], "%Y-%m-%dT%H:%M")
        tasks_number = options["tasks_per_day"]
        day = options["day"]
        prob = options["probability"]
        path = options["path"]

        if day:
            end_date = start_date
            prob = 0

        calendar = create_calendar_if_not_eisit(path, options)

        if not options["add"]:
            old_tasks = Task.objects.filter(calendar=calendar).all()
            if options["verbosity"] >= 2:
                print(f"{len(old_tasks)} was deleted from old calendar")
            old_tasks.delete()

        tasks_counter = 0
        date = start_date
        show_pbar = 1 <= options["verbosity"] <= 2
        if show_pbar:
            pbar = tqdm(total=end_date.timestamp() - start_date.timestamp())
        while date <= end_date:
            number_tasks = generate_day_task_num(tasks_number, prob)
            for i in range(number_tasks):
                date.replace(hour=randint(0, 23))
                create_random_task(date_time=date, calendar=calendar)
                if options["verbosity"] == 3:
                    print(f"Creating task at {date}")
                tasks_counter += 1
            delta = timedelta(days=1)
            if show_pbar:
                pbar.update(delta.total_seconds())
            date.replace(hour=0)
            date += delta
        if show_pbar:
            pbar.close()
        if options["verbosity"] == 0:
            return "OK"
        return f"Created {tasks_counter} tasks for calendar with path {path}."  # TODO Выводить ссылку

    def add_arguments(self, parser):
        parser.add_argument("-s", "--start",
                            type=str,
                            help="Date from which to generate tasks",
                            default="2021-01-01T8:00")
        parser.add_argument("-e",
                            "--end",
                            type=str,
                            help="Date by which to generate tasks", default="2021-12-31T23:55")
        parser.add_argument("-t",
                            "--tasks_per_day",
                            type=int,
                            default=3)
        parser.add_argument("-p", "--probability",
                            type=int,
                            default=70,
                            help="The probability with which the number of tasks will differ from the established one.")
        parser.add_argument("--path",
                            type=str,
                            default="test",
                            help="Path to test calendar")
        parser.add_argument("-a",
                            "--add",
                            action="store_true",
                            help="If this is selected, the tasks will be added to those already existing in the "
                                 "calendar, otherwise the calendar will be recreated")
        parser.add_argument("-d",
                            "--day",
                            action="store_true",
                            help="Add tasks_per_day task to start_day")


def generate_day_task_num(number=3, prob=0.4):
    result = number
    x = rand_100()
    if x > 50:  # 50 на 50 увеличиваем или умееньшаем число задач, а потом с заданной вероятностью изменяем.
        p = rand_100()
        while p <= prob:
            result += 1
            p = rand_100()
    else:
        p = rand_100()
        while p <= prob:
            result -= 1
            p = rand_100()
    if result < 0:
        result = 0
    return result


def create_random_task(calendar: Calendar, date_time: datetime = None, title=None, author=None,
                       description=None):
    if date_time is None:
        date_time = f.date_time()
    if title is None:
        title = f.text(max_nb_chars=60)
    if author is None:
        author = f.name()
    if description is None:
        description = f.text()
    t = Task.objects.create(name=title,
                            description=description,
                            author=author,
                            calendar=calendar,
                            date_time=date_time)
    return t
