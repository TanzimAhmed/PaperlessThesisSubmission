# Generated by Django 3.0.3 on 2020-03-15 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_auto_20200314_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='title',
            field=models.CharField(default='The Solar System', max_length=250),
            preserve_default=False,
        ),
    ]