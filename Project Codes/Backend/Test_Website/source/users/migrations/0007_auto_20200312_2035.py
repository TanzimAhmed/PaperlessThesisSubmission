# Generated by Django 3.0.3 on 2020-03-12 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_verification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='verification',
            old_name='is_verified',
            new_name='is_teacher',
        ),
    ]