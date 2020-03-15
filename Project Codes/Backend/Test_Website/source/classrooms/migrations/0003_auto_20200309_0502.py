# Generated by Django 3.0.3 on 2020-03-09 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classrooms', '0002_auto_20200308_1956'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='classroom',
            constraint=models.UniqueConstraint(fields=('course_code', 'section', 'semester'), name='unique_classroom'),
        ),
    ]