# Generated by Django 3.0.3 on 2020-03-13 13:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('classrooms', '0004_quiz_is_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='time_stamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 3, 13, 13, 38, 50, 398028, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='is_running',
            field=models.BooleanField(default=False),
        ),
    ]
