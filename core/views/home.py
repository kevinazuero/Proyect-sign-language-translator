from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from core.utils.text_to_speech import text_to_speech
import json
from django.shortcuts import redirect


@login_required
def mostrar_html(request):
    return render(request, 'home.html', {
        'user': request.user,
    })

@login_required
def text_speech(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '')

        if text:
            text_to_speech(text)
            return JsonResponse({"message": "Exito"})
        else:
            return JsonResponse({"error": "No hay texto"}, status=400)

    return redirect('core:inicio')

