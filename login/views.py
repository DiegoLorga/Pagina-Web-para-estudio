from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Estudiante

def login_view(request):
    return render(request, 'login.html')

def lista_view(request):
    # Vista protegida: sólo estudiantes logueados
    if 'usuario_id' not in request.session:
        return redirect('login')
    context = {}
    return render(request, 'lista.html', context)

def registro_estudiante(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        if nombre and correo and password:
            if Estudiante.objects.filter(correo=correo).exists():
                context = {'error': "Este correo ya está registrado."}
                return render(request, 'login.html', context)
            else:
                estudiante = Estudiante.objects.create(
                    nombre=nombre,
                    correo=correo,
                    password=make_password(password),
                    rachaDias=0
                )
                # 🚀 Loguear automáticamente al usuario
                request.session['usuario_id'] = estudiante.id
                request.session['usuario_nombre'] = estudiante.nombre
                return redirect('lista_view')
    return render(request, 'login.html')

def login_estudiante(request):
    context = {}

    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        try:
            estudiante = Estudiante.objects.get(correo=correo)
            if check_password(password, estudiante.password):
                request.session['usuario_id'] = estudiante.id
                request.session['usuario_nombre'] = estudiante.nombre
                return redirect('lista_view')
            else:
                context['error_login'] = "Contraseña incorrecta."
        except Estudiante.DoesNotExist:
            context['error_login'] = "Este usuario no tiene una cuenta registrada."

    return render(request, 'login.html', context)
