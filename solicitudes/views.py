# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Solicitud
from .forms import SolicitudForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm



@login_required
def lista_solicitudes(request):
    if request.user.is_superuser:
        solicitudes = Solicitud.objects.all()
    else:
        solicitudes = Solicitud.objects.filter(estado='Pendiente')
    return render(request, 'solicitudes/lista_solicitudes.html', {'solicitudes': solicitudes})

@login_required
def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.save()
            return redirect('lista_solicitudes')
    else:
        form = SolicitudForm()
    return render(request, 'solicitudes/crear_solicitud.html', {'form': form})

@login_required
def aprobar_solicitud(request, solicitud_id):
    if request.user.is_superuser:
        solicitud = get_object_or_404(Solicitud, id=solicitud_id)
        solicitud.estado = 'Aprobado'
        solicitud.save()
    return redirect('lista_solicitudes')

@login_required
def rechazar_solicitud(request, solicitud_id):
    if request.user.is_superuser:
        solicitud = get_object_or_404(Solicitud, id=solicitud_id)
        solicitud.estado = 'Rechazado'
        solicitud.save()
    return redirect('lista_solicitudes')

#Usuarios

@login_required
def lista_usuarios(request):
    if not request.user.is_superuser:
        return redirect('lista_solicitudes')
    usuarios = User.objects.all()
    return render(request, 'solicitudes/lista_usuarios.html', {'usuarios': usuarios})

@login_required
def crear_usuario(request):
    if not request.user.is_superuser:
        return redirect('lista_solicitudes')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UserCreationForm()
    return render(request, 'solicitudes/crear_usuario.html', {'form': form})

@login_required
def cambiar_contrasena(request, usuario_id):
    if not request.user.is_superuser:
        return redirect('lista_solicitudes')
    usuario = get_object_or_404(User, id=usuario_id)
    if request.method == 'POST':
        form = PasswordChangeForm(user=usuario, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = PasswordChangeForm(user=usuario)
    return render(request, 'solicitudes/cambiar_contrasena.html', {'form': form, 'usuario': usuario})
