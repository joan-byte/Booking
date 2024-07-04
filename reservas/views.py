# reservas/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.utils import timezone
from .forms import RegistroForm, ReservaForm, JugadorFormSet
from .models import Pista, Reserva

# Verificar si el usuario es superuser
def superuser_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func

def index(request):
    reservas = Reserva.objects.filter(fecha_hora_inicio__gte=timezone.now(), fecha_hora_inicio__lte=timezone.now() + timezone.timedelta(days=1))
    return render(request, 'reservas/index.html', {'reservas': reservas})

@login_required
def reservar(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        formset = JugadorFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            reserva = form.save(commit=False)
            reserva.socio = request.user
            jugadores = []
            for jugador_form in formset:
                if jugador_form.cleaned_data:
                    jugador = {
                        'nombre': jugador_form.cleaned_data.get('nombre'),
                        'apellido': jugador_form.cleaned_data.get('apellido'),
                        'tipo': jugador_form.cleaned_data.get('tipo'),
                    }
                    jugadores.append(jugador)
            reserva.jugadores = jugadores
            reserva.fecha_hora_fin = reserva.fecha_hora_inicio + timezone.timedelta(hours=1) if reserva.pista.tipo == 'tenis' else timezone.timedelta(hours=1, minutes=15)
            reserva.save()
            return redirect('reservation_list')
    else:
        form = ReservaForm()
        formset = JugadorFormSet()
    return render(request, 'reservas/reserve.html', {'form': form, 'formset': formset})

@login_required
def reservation_list(request):
    reservas = Reserva.objects.filter(socio=request.user)
    return render(request, 'reservas/reservation_list.html', {'reservas': reservas})

@superuser_required
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            grupo = form.cleaned_data.get('tipo')
            group = Group.objects.get(name=grupo)
            user.groups.add(group)
            return redirect('index')
    else:
        form = RegistroForm()
    return render(request, 'reservas/registro.html', {'form': form})