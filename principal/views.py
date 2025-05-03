from django.shortcuts import render, redirect
from tareas.models import Tarea  # Asegúrate que esta línea esté presente

def menu_principal(request):
    usuario_id = request.session.get('usuario_id')  # recupera el id del usuario logueado
    if not usuario_id:
        return redirect('login')  # si no está logueado, mándalo a login

    # Obtener las tareas del usuario
    tareas = Tarea.objects.filter(usuarioid_id=usuario_id).order_by('-fecha_creacion')

    return render(request, 'menu_principal.html', {
        'usuario_id': usuario_id,
        'tareas': tareas
    })
