from django.shortcuts import render, redirect
from login.models import Estudiante
from django.http import JsonResponse
from django.utils import timezone
from PyPDF2 import PdfReader
from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

def menu_principal(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    try:
        usuario = Estudiante.objects.get(id=usuario_id)
    except Estudiante.DoesNotExist:
        return redirect('login')

    hoy = timezone.now().date()
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

def procesar_pdf(request):
    if request.method == "POST":
        archivo = request.FILES.get("archivo")
        accion = request.POST.get("accion")

        if not archivo or not archivo.name.endswith(".pdf"):
            return JsonResponse({"error": "Por favor, sube un archivo PDF válido."}, status=400)

        try:
            reader = PdfReader(archivo)
            texto = ""
            for pagina in reader.pages:
                extraido = pagina.extract_text()
                if extraido:
                    texto += extraido

            if not texto.strip():
                return JsonResponse({"error": "No se pudo extraer texto del PDF."}, status=400)

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

            resultado = llm.invoke(prompt)
            return JsonResponse({"resultado": resultado})

        except Exception as e:
            return JsonResponse({"error": f"Ocurrió un error al procesar el archivo: {str(e)}"}, status=500)

    return JsonResponse({"error": "Solicitud inválida."}, status=400)
