from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def sign_in(request):
    
    if request.user.is_authenticated:
        return redirect('core:inicio')

    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm(),
            'options':'Crear cuenta',
            'enlace': 'core:registrar'})
         
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']
        )
        if user is None:
            return render(request, 'login.html', {
            'form': AuthenticationForm(),
            'titulo': 'inicio de sesion',
            'options':'Crear cuenta',
            'botom': 'Inicio de sesion',
            'enlace': 'core:registrar',
            'error': 'El nombre o la contraseña del usuario son incorrectas'})
        else:
            login(request, user)
            return redirect('core:inicio')
        

@login_required
def log_out(request): #Go out
    logout(request)
    return redirect('login')




