# Generated by Django 3.2.19 on 2023-05-19 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservation_app', '0014_alter_evenment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='evenment',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]
