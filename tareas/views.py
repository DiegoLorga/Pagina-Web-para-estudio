from django.shortcuts import render, redirect, get_object_or_404
from .models import Tarea
from login.models import Estudiante  # Asegúrate que este sea el correcto
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import JsonResponse

def tareas_view(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    usuario_id = request.session['usuario_id']
    tareas = Tarea.objects.filter(usuarioid_id=usuario_id).order_by('-fecha_creacion')
    return render(request, 'menu_principal.html', {'tareas': tareas})

def crear_tarea(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        try:
            usuario = Estudiante.objects.get(id=request.session['usuario_id'])
        except Estudiante.DoesNotExist:
            return HttpResponse(status=400)

        tarea = Tarea.objects.create(
            usuarioid=usuario,
            titulo=request.POST.get('titulo'),
            descripcion=request.POST.get('descripcion', ''),
            estado=int(request.POST.get('estado', 0))
        )

        # Renderiza solo la nueva tarea como fragmento
        html = render_to_string('partials/tarea.html', {'tarea': tarea}, request=request)
        return JsonResponse({'html': html})


@csrf_exempt
def actualizar_tarea(request, tarea_id):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        nuevo_estado = int(data.get('estado', 0))

        tarea = Tarea.objects.get(id=tarea_id)
        tarea.estado = nuevo_estado
        tarea.save()

        return JsonResponse({'estado': tarea.estado, 'id': tarea.id})
