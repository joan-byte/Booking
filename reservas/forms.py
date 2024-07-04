# /mnt/data/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Reserva

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    TIPO_SOCIO = (
        ('Socios Deportivos', 'Socios Deportivos'),
        ('Socios Paseantes', 'Socios Paseantes'),
    )
    tipo = forms.ChoiceField(choices=TIPO_SOCIO)
    telefono = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'tipo', 'telefono']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class JugadorForm(forms.Form):
    nombre = forms.CharField(max_length=30, label='Nombre')
    apellido = forms.CharField(max_length=30, label='Apellido')
    TIPO_JUGADOR = (
        ('deportivo', 'Socio Deportivo'),
        ('no_deportivo', 'Socio No Deportivo'),
        ('no_socio', 'No Socio'),
    )
    tipo = forms.ChoiceField(choices=TIPO_JUGADOR, label='Tipo de Jugador')

JugadorFormSet = forms.formset_factory(JugadorForm, extra=2)

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['pista', 'fecha_hora_inicio']
        widgets = {
            'fecha_hora_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }