from django.shortcuts import render, redirect

def menu_principal(request):
    usuario_id = request.session.get('usuario_id')  # recupera el id del usuario logueado
    if not usuario_id:
        return redirect('login')  # si no está logueado, mándalo a login

    return render(request, 'menu_principal.html', {'usuario_id': usuario_id}) 