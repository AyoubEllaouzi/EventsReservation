# Generated by Django 3.2.19 on 2023-06-23 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservation_app', '0029_alter_evenment_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_event', models.CharField(max_length=50, null=True)),
                ('date_event', models.DateTimeField(null=True)),
                ('lieu_event', models.CharField(max_length=50, null=True)),
                ('vue', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]