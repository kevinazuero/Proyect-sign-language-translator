from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from core.models import User
from django.shortcuts import render, redirect
from django.db import IntegrityError
from core.utils.utils import generate_unique_username


def register(request):
    if request.method == 'POST':
        if request.POST.get('password1') == request.POST.get('password2'):
            try:
                new_user_name = generate_unique_username(request.POST.get('nombres'))
                user = User.objects.create_user(username=new_user_name,
                                                first_name=request.POST.get('nombres'),
                                                last_name=request.POST.get('apellidos'),
                                                email=request.POST.get('email'),
                                                password=request.POST.get('password1'))
                user.save()
                user = authenticate(request, username=new_user_name, password=request.POST.get('password1'))
                if user is not None:
                    login(request, user)
                    return redirect('core:inicio')
                else:
                    return HttpResponse("La autenticación falló después de crear el usuario.")
            except IntegrityError:
                return render(request, 'signup.html',
                              {'error': 'Este usuario ya existe.', 'enlace': 'login', 'options': 'Iniciar sesion'})
            except Exception as e:
                return HttpResponse('Error: {}'.format(str(e)))
        else:
            return render(request, 'signup.html',
                          {'enlace': 'login', 'options': 'Iniciar sesion', 'error': 'Las contraseñas no coinciden.'})

    else:
        return render(request, 'signup.html', {'enlace': 'login', 'options': 'Iniciar sesion'})
