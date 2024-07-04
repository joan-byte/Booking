# reservas/models.py

from django.db import models
from django.contrib.auth.models import User

class Pista(models.Model):
    TIPO_PISTA = (
        ('tenis', 'Tenis'),
        ('padel', 'Padel'),
    )
    tipo = models.CharField(max_length=5, choices=TIPO_PISTA)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    socio = models.ForeignKey(User, on_delete=models.CASCADE)
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField()
    jugadores = models.JSONField(default=list)

    def __str__(self):
        return f"Reserva de {self.socio} en {self.pista} el {self.fecha_hora_inicio}"