from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages



@login_required
def edit_user(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        user = request.user
    
        if not current_password:
            messages.error(request, 'Por favor ingrese su contraseña actual para guardar los cambios.')
            return redirect('core:editar')

        if not user.check_password(current_password):
            messages.error(request, 'Contraseña incorrecta.')
            return redirect('core:editar')

        if 'image' in request.FILES:
            user.image = request.FILES['image']
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)

        if new_password:
            user.set_password(new_password)
            update_session_auth_hash(request, user)  # Mantener la sesión después de cambiar la contraseña

        user.save()
        return redirect('core:editar')

    return render(request, 'editperfil.html', {'user': request.user,})