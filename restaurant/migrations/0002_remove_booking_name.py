# Generated by Django 4.1.7 on 2023-03-31 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='name',
        ),
    ]
