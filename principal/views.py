from django.shortcuts import render, redirect
from login.models import Estudiante
from django.http import JsonResponse
from django.utils import timezone
from PyPDF2 import PdfReader
from langchain_community.llms import Ollama
from tareas.models import Tarea

# Instancia del modelo de lenguaje Ollama
llm = Ollama(model="llama3")

# Vista principal del menú después de iniciar sesión
def menu_principal(request):
    usuario_id = request.session.get('usuario_id')  # Obtiene el ID del usuario desde la sesión
    if not usuario_id:
        return redirect('login')  # Si no hay sesión, redirige a login
    try:
        usuario = Estudiante.objects.get(id=usuario_id)  # Obtiene el objeto Estudiante
    except Estudiante.DoesNotExist:
        return redirect('login')  # Si no existe, redirige a login

    hoy = timezone.now().date()
    ya_cumplio = usuario.ultima_actividad == hoy  # Verifica si ya hizo actividad hoy

    return render(request, 'menu_principal.html', {
        'usuario': usuario,
        'ya_cumplio': ya_cumplio
    })

# Vista para aumentar el contador de racha del usuario
def aumentar_racha(request):
    if request.method == "POST":
        usuario_id = request.session.get('usuario_id')  # Verifica sesión
        if not usuario_id:
            return JsonResponse({'ok': False, 'error': 'Usuario no autenticado'}, status=401)

        try:
            estudiante = Estudiante.objects.get(id=usuario_id)  # Busca al estudiante
        except Estudiante.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Usuario no encontrado'}, status=404)

        hoy = timezone.now().date()
        ayer = hoy - timezone.timedelta(days=1)

        # Lógica para aumentar la racha
        if estudiante.ultima_actividad is None:
            estudiante.rachaDias = 1
        elif estudiante.ultima_actividad == ayer:
            estudiante.rachaDias += 1

        estudiante.ultima_actividad = hoy  # Actualiza última actividad
        estudiante.save()

        return JsonResponse({'ok': True, 'racha': estudiante.rachaDias})

# Vista que procesa un archivo PDF y genera resumen o cuestionario
def procesar_pdf(request):
    if request.method == "POST":
        archivo = request.FILES.get("archivo")  # Archivo recibido desde el formulario
        accion = request.POST.get("accion")  # Acción solicitada: resumen o cuestionario

        # Validación del archivo
        if not archivo or not archivo.name.endswith(".pdf"):
            return JsonResponse({"error": "Por favor, sube un archivo PDF válido."}, status=400)

        try:
            reader = PdfReader(archivo)  # Lector de PDF
            texto = ""
            for pagina in reader.pages:
                extraido = pagina.extract_text()  # Extrae texto de cada página
                if extraido:
                    texto += extraido

            if not texto.strip():
                return JsonResponse({"error": "No se pudo extraer texto del PDF."}, status=400)

            # Construcción del prompt según la acción
            if accion == "resumen":
                prompt = f"Resume el siguiente texto:\n\n{texto}"
            elif accion == "cuestionario":
                prompt = (
                    "Crea un cuestionario con al menos 5 preguntas sobre el siguiente texto. "
                    "Devuélvelo en formato JSON como una lista. Cada elemento debe tener:\n"
                    "- 'pregunta': la pregunta en texto\n"
                    "- 'opciones': un objeto con claves 'a', 'b', 'c', 'd' y sus respectivos textos\n"
                    "- 'respuesta_correcta': una de las letras 'a', 'b', 'c' o 'd'\n"
                    "Devuelve SOLO el JSON, sin ningún texto adicional.\n\n"
                    f"Texto:\n{texto}"
                )
            else:
                return JsonResponse({"error": "Acción no válida."}, status=400)

            # Invoca el modelo de lenguaje con el prompt generado
            resultado = llm.invoke(prompt)
            return JsonResponse({"resultado": resultado})

        except Exception as e:
            # Manejo de errores en la lectura o procesamiento del archivo
            return JsonResponse({"error": f"Ocurrió un error al procesar el archivo: {str(e)}"}, status=500)

    # Si no es POST, devuelve error
    return JsonResponse({"error": "Solicitud inválida."}, status=400)

    # Este bloque es inalcanzable por estar después de un return
    tareas = Tarea.objects.filter(usuarioid_id=usuario_id).order_by('-fecha_creacion')
    return render(request, 'menu_principal.html', {
        'usuario_id': usuario_id,
        'tareas': tareas
    })
