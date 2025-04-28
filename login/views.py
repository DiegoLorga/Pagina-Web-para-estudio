from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Estudiante

def login_view(request):
    return render(request, 'login.html')  # Solo muestra el formulario

def registro_estudiante(request):
    context = {}

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        if nombre and correo and password:
            if Estudiante.objects.filter(correo=correo).exists():
                context['error'] = "Este correo ya está registrado."
            else:
                Estudiante.objects.create(
                    nombre=nombre,
                    correo=correo,
                    password=make_password(password),
                    rachaDias=0
                )
                context['exito'] = "Registro exitoso. ¡Ahora puedes iniciar sesión!"

    return render(request, 'login.html', context)

def login_estudiante(request):
    context = {}

    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        try:
            estudiante = Estudiante.objects.get(correo=correo)
            if check_password(password, estudiante.password):
                request.session['usuario_id'] = estudiante.id
                return redirect('menu_principal')  # 🔥 Aquí debes tener tu vista de menú
            else:
                context['error_login'] = "Contraseña incorrecta."
        except Estudiante.DoesNotExist:
            context['error_login'] = "Este usuario no tiene una cuenta registrada."

    return render(request, 'login.html', context)