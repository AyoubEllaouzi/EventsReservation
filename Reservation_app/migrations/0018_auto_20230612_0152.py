# Generated by Django 3.2.19 on 2023-06-12 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reservation_app', '0017_evenment_nbr_ticket_max'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='is_valable',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='nbr_ticket',
        ),
    ]