# Generated by Django 3.0.3 on 2020-03-12 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_is_educator'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('username', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=10)),
                ('is_verified', models.BooleanField(default=False)),
                ('time_stamp', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
