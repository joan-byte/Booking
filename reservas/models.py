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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()