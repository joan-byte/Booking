from django import forms
from django.contrib.auth.models import User
from .models import Reserva, Pista

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
        ('no_deportivo', 'Socio Paseante'),
        ('no_socio', 'No Socio'),
    )
    tipo = forms.ChoiceField(choices=TIPO_JUGADOR, label='Tipo de Jugador')

class ReservaForm(forms.ModelForm):
    fecha_hora_inicio = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Reserva
        fields = ['pista', 'fecha_hora_inicio']

    def clean(self):
        cleaned_data = super().clean()
        pista = cleaned_data.get('pista')
        total_jugadores = int(self.data.get('form-TOTAL_FORMS', 0))

        # Contar solo los formularios que tienen datos válidos
        jugadores_validos = sum(
            1 for i in range(total_jugadores)
            if self.data.get(f'form-{i}-nombre') and self.data.get(f'form-{i}-apellido')
        )

        if pista and pista.tipo == 'padel' and jugadores_validos != 4:
            self.add_error(None, 'Debe haber 4 jugadores para reservar una pista de pádel.')
        if pista and pista.tipo == 'tenis' and jugadores_validos not in [2, 4]:
            self.add_error(None, 'Debe haber 2 o 4 jugadores para reservar una pista de tenis.')

        return cleaned_data