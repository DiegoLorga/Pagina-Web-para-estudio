from django.shortcuts import render, redirect, get_object_or_404
from .models import Tarea
from login.models import Estudiante  # Modelo del usuario
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse

# Vista principal para mostrar las tareas del usuario
def tareas_view(request):
    if 'usuario_id' not in request.session:
        return redirect('login')  # Si no hay sesión, redirige a login

    usuario_id = request.session['usuario_id']
    # Filtra las tareas del usuario por fecha de creación descendente
    tareas = Tarea.objects.filter(usuarioid_id=usuario_id).order_by('-fecha_creacion')
    return render(request, 'menu_principal.html', {'tareas': tareas})  # Reutiliza el menú principal como vista

# Vista para crear una nueva tarea desde el formulario
def crear_tarea(request):
    if 'usuario_id' not in request.session:
        return redirect('login')  # Valida sesión

    if request.method == 'POST':
        try:
            usuario = Estudiante.objects.get(id=request.session['usuario_id'])  # Obtiene al estudiante
        except Estudiante.DoesNotExist:
            return HttpResponse(status=400)  # Si no existe, devuelve error

        # Crea la nueva tarea con los datos del formulario
        tarea = Tarea.objects.create(
            usuarioid=usuario,
            titulo=request.POST.get('titulo'),
            descripcion=request.POST.get('descripcion', ''),
            estado=int(request.POST.get('estado', 0))
        )

        # Renderiza la nueva tarea como fragmento HTML para insertar dinámicamente
        html = render_to_string('partials/tarea.html', {'tarea': tarea}, request=request)
        return JsonResponse({'html': html})  # Retorna el HTML como respuesta JSON

# Vista para actualizar el estado de una tarea (usada con AJAX)
@csrf_exempt  # Exime la protección CSRF para permitir solicitudes desde JS
def actualizar_tarea(request, tarea_id):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)  # Parsea el cuerpo de la solicitud
        nuevo_estado = int(data.get('estado', 0))  # Obtiene el nuevo estado

        tarea = Tarea.objects.get(id=tarea_id)  # Busca la tarea por ID
        tarea.estado = nuevo_estado  # Actualiza el estado
        tarea.save()  # Guarda los cambios

        # Devuelve el nuevo estado y el ID como JSON
        return JsonResponse({'estado': tarea.estado, 'id': tarea.id})
