# Generated by Django 3.0.3 on 2020-03-08 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_auto_20200307_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='information',
            field=models.CharField(max_length=250, null=True),
        ),
    ]