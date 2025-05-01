from django.shortcuts import render, redirect
from login.models import Estudiante
from django.http import JsonResponse
from django.utils import timezone

def menu_principal(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    try:
        usuario = Estudiante.objects.get(id=usuario_id)
    except Estudiante.DoesNotExist:
        return redirect('login')

    # Obtener la fecha de hoy
    hoy = timezone.now().date()

    # Verificar si ya cumplió la racha hoy
    ya_cumplio = usuario.ultima_actividad == hoy

    return render(request, 'menu_principal.html', {
        'usuario': usuario,
        'ya_cumplio': ya_cumplio  
    })

def aumentar_racha(request):
    if request.method == "POST":
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return JsonResponse({'ok': False, 'error': 'Usuario no autenticado'}, status=401)

        try:
            estudiante = Estudiante.objects.get(id=usuario_id)
        except Estudiante.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Usuario no encontrado'}, status=404)

        hoy = timezone.now().date()

        if estudiante.ultima_actividad != hoy:
            if estudiante.ultima_actividad == hoy - timezone.timedelta(days=1):
                estudiante.rachaDias += 1
            else:
                estudiante.rachaDias = 1

            estudiante.ultima_actividad = hoy
            estudiante.save()

        return JsonResponse({'ok': True, 'racha': estudiante.rachaDias})
