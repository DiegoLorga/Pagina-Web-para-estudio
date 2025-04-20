from django.shortcuts import render

def timer(request):
    return render(request, 'temporizador/timer.html')