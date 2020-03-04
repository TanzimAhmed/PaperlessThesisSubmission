# Generated by Django 3.0.3 on 2020-03-04 00:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200302_1137'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=30)),
                ('section', models.IntegerField()),
                ('name', models.CharField(max_length=128)),
                ('upload', models.BooleanField()),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='group',
            constraint=models.UniqueConstraint(fields=('course_code', 'section', 'name'), name='unique_group'),
        ),
    ]
