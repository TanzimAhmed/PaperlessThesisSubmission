# Generated by Django 3.0.3 on 2020-04-06 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classrooms', '0008_resource'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resource',
            old_name='user',
            new_name='quiz',
        ),
    ]
