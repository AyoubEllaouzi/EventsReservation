# Generated by Django 3.2.19 on 2023-06-12 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservation_app', '0018_auto_20230612_0152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='user',
        ),
        migrations.AddField(
            model_name='reservation',
            name='user_email',
            field=models.CharField(max_length=50, null=True),
        ),
    ]