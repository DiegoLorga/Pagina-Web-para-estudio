from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Estudiante
from django.utils import timezone

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
                return redirect('')
    return render(request, 'login.html')

def login_estudiante(request):
    context = {}

    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        try:
            estudiante = Estudiante.objects.get(correo=correo)
            if check_password(password, estudiante.password):
                # ✅ Verificar racha 
                hoy = timezone.now().date()
                ayer = hoy - timezone.timedelta(days=1)

                if estudiante.ultima_actividad:
                    if estudiante.ultima_actividad < ayer and estudiante.rachaDias > 0:
                        estudiante.rachaDias = 0
                        estudiante.save()
                        context['racha_reiniciada'] = True  # puedes usar esto en la plantilla

                request.session['usuario_id'] = estudiante.id
                request.session['usuario_nombre'] = estudiante.nombre
                return redirect('menu_principal')
            else:
                context['error_login'] = "Contraseña incorrecta."
        except Estudiante.DoesNotExist:
            context['error_login'] = "Este usuario no tiene una cuenta registrada."

    return render(request, 'login.html', context);