# Generated by Django 4.1.7 on 2023-03-31 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_remove_booking_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='name',
            field=models.CharField(default='lukas', max_length=100),
            preserve_default=False,
        ),
    ]
