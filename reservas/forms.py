from django import forms
from django.contrib.auth.models import User
from .models import Reserva, Pista

class RegistroForm(forms.ModelForm):
    tipo = forms.ChoiceField(choices=[('deportivo', 'Socio Deportivo'), ('paseante', 'Socio Paseante')])

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput(),
        }

    telefono = forms.CharField(max_length=15)

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['pista', 'fecha_hora_inicio']
        widgets = {
            'fecha_hora_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class JugadorForm(forms.Form):
    nombre = forms.CharField(required=False)
    apellido = forms.CharField(required=False)
    tipo = forms.ChoiceField(choices=[('deportivo', 'Socio Deportivo'), ('paseante', 'Socio Paseante'), ('no_socio', 'No Socio')], required=False)