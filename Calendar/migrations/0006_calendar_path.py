# Generated by Django 3.2.3 on 2021-05-28 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Calendar', '0005_remove_calendar_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='path',
            field=models.CharField(default=0, help_text='Путь по которому получают этот календарь', max_length=63, unique=True),
            preserve_default=False,
        ),
    ]
