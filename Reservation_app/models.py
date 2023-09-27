from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Client(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=500, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)


class Organiseur(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=500, null=True)
    picture = models.ImageField(default='test.jpeg', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)


class Evenment(models.Model):
    id_organ = models.IntegerField(null=True)
    name = models.CharField(max_length=50, null=True)
    date = models.DateTimeField(null=True)
    lieu = models.CharField(max_length=50, null=True)
    type = models.CharField(max_length=50, null=True)
    price = models.FloatField(null=True)
    nbr_ticket_max = models.IntegerField(null=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    picture = models.ImageField(default='m.jpg', null=True, blank=True)
    is_Vaide = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    evenment = models.ForeignKey(Evenment, null=True, on_delete=models.SET_NULL)
    user_email = models.CharField(max_length=50, null=True)
    type_event = models.CharField(max_length=50, null=True)
    nbr_ticket = models.IntegerField(null=True)
    montant = models.FloatField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user_email


class Payment(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    montant = models.FloatField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "Payment"


class Notification(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    name_event = models.CharField(max_length=50, null=True)
    date_event = models.DateTimeField(null=True)
    lieu_event = models.CharField(max_length=50, null=True)
    vue = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "Notification"
