# Generated by Django 3.0.3 on 2020-03-08 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classrooms', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performance',
            old_name='students',
            new_name='student',
        ),
        migrations.AlterField(
            model_name='performance',
            name='response',
            field=models.CharField(default='', max_length=25),
        ),
    ]
