# Generated by Django 3.2.19 on 2023-06-23 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservation_app', '0027_evenment_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evenment',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
