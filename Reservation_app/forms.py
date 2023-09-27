from django.forms import ModelForm
from Reservation_app.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class CreatUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# __________________________________________________
class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Evenment
        fields = ['name', 'date', 'lieu', 'type', 'price', 'nbr_ticket_max', 'description', 'picture']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class EventForm(ModelForm):
    class Meta:
        model = Evenment
        fields = '__all__'


class SettingOrganisation(forms.ModelForm):
    class Meta:
        model = Organiseur
        fields = ['picture']

