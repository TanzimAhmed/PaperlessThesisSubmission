# Generated by Django 3.0.3 on 2020-03-04 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learners', '0001_initial'),
        ('documents', '0002_auto_20200304_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learners.Group'),
        ),
    ]
