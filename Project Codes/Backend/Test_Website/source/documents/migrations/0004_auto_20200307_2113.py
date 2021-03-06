# Generated by Django 3.0.3 on 2020-03-07 21:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20200304_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='instructor',
        ),
        migrations.RemoveField(
            model_name='document',
            name='status',
        ),
        migrations.AddField(
            model_name='document',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='document',
            name='date_uploaded',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
