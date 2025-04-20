from django.shortcuts import render
from PyPDF2 import PdfReader
from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

def procesar_pdf(request):
    resultado = None

    if request.method == "POST":
        archivo = request.FILES.get("archivo")
        accion = request.POST.get("accion")

        if archivo and archivo.name.endswith(".pdf"):
            reader = PdfReader(archivo)
            texto = ""
            for pagina in reader.pages:
                texto += pagina.extract_text()

            if accion == "resumen":
                prompt = f"Resume el siguiente texto:\n\n{texto}"
            elif accion == "cuestionario":
                prompt = f"Crea un cuestionario que se responda con el siguiente texto:\n\n{texto}"
            else:
                prompt = ""

            resultado = llm.invoke(prompt)

    return render(request, "llamaapp/index.html", {"resultado": resultado})