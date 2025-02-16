from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def menu_training_view(request):
    return render(request, 'menu_training.html', {
        'user': request.user,
    })