from django.shortcuts import render
from django.http import JsonResponse
from .models import Agenda
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
import json
from datetime import datetime

def agenda_view(request):
    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        return redirect('login')  # Si no está logueado, regresa al login

    return render(request, 'eventosAgenda/agenda.html', {'usuario_id': usuario_id})


# Obtener eventos a partir de una fecha
def obtener_eventos_desde_fecha(request, fecha):
    eventos = Agenda.objects.filter(fecha_evento__gte=fecha).values()
    return JsonResponse(list(eventos), safe=False)

# Crear un nuevo evento
@csrf_exempt
def crear_evento(request):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        print("ID de usuario recibido:", data.get('usuarioid'))

        try:
            agenda = Agenda.objects.create(
                usuarioid_id=data['usuarioid'],  # usa _id para indicar que es el valor de la FK
                titulo=data['titulo'],
                descripcion=data['descripcion'],
                fecha_evento=data['fecha_evento'],
                importante=data.get('importante', False)
            )
            return JsonResponse({'mensaje': 'Evento creado', 'id': agenda.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Eliminar evento por ID
@csrf_exempt
def eliminar_evento(request, evento_id):
    if request.method == 'DELETE':
        try:
            evento = Agenda.objects.get(id=evento_id)
            evento.delete()
            return JsonResponse({'mensaje': 'Evento eliminado'})
        except Agenda.DoesNotExist:
            return JsonResponse({'error': 'Evento no encontrado'}, status=404)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Editar un evento
@csrf_exempt
def editar_evento(request, evento_id):
    if request.method == 'PUT':
        try:
            evento = Agenda.objects.get(id=evento_id)
            data = json.loads(request.body)
            evento.titulo = data.get('titulo', evento.titulo)
            evento.descripcion = data.get('descripcion', evento.descripcion)
            evento.fecha_evento = data.get('fecha_evento', evento.fecha_evento)
            evento.importante = data.get('importante', evento.importante)
            evento.save()
            return JsonResponse({'mensaje': 'Evento actualizado'})
        except Agenda.DoesNotExist:
            return JsonResponse({'error': 'Evento no encontrado'}, status=404)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def obtener_eventos_usuario(request):
    usuario_id = request.session.get('usuario_id')
    
    if not usuario_id:
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

    eventos = Agenda.objects.filter(usuarioid_id=usuario_id).values(
        'id', 'titulo', 'descripcion', 'fecha_evento', 'importante'
    )
    return JsonResponse(list(eventos), safe=False)