from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.db.models import Q
from django import forms
from .forms import RegistroForm, ReservaForm, JugadorForm
from .models import Pista, Reserva, Profile

@login_required
def index(request):
    now = timezone.now()
    end_time = now + timezone.timedelta(days=1)
    pistas = Pista.objects.all()
    horas_del_dia = [now.replace(hour=h, minute=m, second=0, microsecond=0) for h in range(24) for m in (0, 15, 30, 45)]
    reservas = Reserva.objects.filter(fecha_hora_inicio__gte=now, fecha_hora_inicio__lte=end_time)

    reservas_por_pista = {pista.nombre: {hora: None for hora in horas_del_dia} for pista in pistas}
    for reserva in reservas:
        pista_nombre = reserva.pista.nombre
        hora_inicio = reserva.fecha_hora_inicio.replace(second=0, microsecond=0, tzinfo=None)
        reservas_por_pista[pista_nombre][hora_inicio] = reserva

    return render(request, 'reservas/index.html', {
        'reservas_por_pista': reservas_por_pista,
        'horas_del_dia': horas_del_dia,
        'now': now
    })

@login_required
def reservar(request):
    JugadorFormSet = forms.formset_factory(JugadorForm, extra=4)

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            pista = form.cleaned_data.get('pista')
            JugadorFormSet = forms.formset_factory(JugadorForm, extra=4 if pista.tipo == 'padel' else 4)
            formset = JugadorFormSet(request.POST)

            if formset.is_valid():
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

                print("Fecha y hora de inicio (datetime):", reserva.fecha_hora_inicio)

                reserva.fecha_hora_fin = reserva.fecha_hora_inicio + (timezone.timedelta(hours=1) if reserva.pista.tipo == 'tenis' else timezone.timedelta(hours=1, minutes=15))
                reserva.save()
                print("Reserva guardada:", reserva)
                return redirect('reservation_list')
            else:
                print("Formset no es válido:", formset.errors)
        else:
            print("Formulario no es válido:", form.errors)
            formset = JugadorFormSet(request.POST)
    else:
        form = ReservaForm()
        formset = JugadorFormSet()

    print("Tipo de fecha_hora_inicio:", type(request.POST.get('fecha_hora_inicio')))
    print("Valor de fecha_hora_inicio:", request.POST.get('fecha_hora_inicio'))

    return render(request, 'reservas/reserve.html', {'form': form, 'formset': formset})

@login_required
def reservation_list(request):
    usuario = request.user
    reservas = Reserva.objects.filter(Q(socio=usuario) | Q(jugadores__icontains=usuario.first_name))

    return render(request, 'reservas/reservation_list.html', {'reservas': reservas})

@user_passes_test(lambda u: u.is_superuser)
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user, telefono=form.cleaned_data.get('telefono'))
            grupo = form.cleaned_data.get('tipo')
            group = Group.objects.get(name=grupo)
            user.groups.add(group)
            return redirect('index')
    else:
        form = RegistroForm()
    return render(request, 'reservas/registro.html', {'form': form})