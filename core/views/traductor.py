from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from core.utils.text_to_speech import text_to_speech
import json
from django.shortcuts import redirect
from core.utils.helpers import get_actions
import os

from core.utils.constants import DATA_PATH, FRAME_ACTIONS_PATH, ROOT_PATH
from core.utils.helpers import count_samples
from core.models import Words_state
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView




@login_required
def mostrar_html(request):
    return render(request, 'home.html', {
        'user': request.user,
    })

@login_required
def training_view(request):
    root = os.getcwd()
    data_path = os.path.join(root, "data")
    actions = get_actions(data_path)  # ['word1', 'word2', 'word3']
    return render(request, 'training.html', {
        'user': request.user,
        'actions':actions,
    })
    
@login_required
def menu_training_view(request):
    return render(request, 'menu_training.html', {
        'user': request.user,
    })
    
@login_required
def getting_keypoints_view(request):
    root = os.getcwd()
    data_path = os.path.join(root, "data")
    actions = get_actions(data_path)
    words_path = os.path.join(ROOT_PATH, FRAME_ACTIONS_PATH)
    info = []
        
    # Generar keypoints solo para palabras nuevas
    for word_name in os.listdir(words_path):
        count=count_samples(word_name)
        if word_name in actions:
            estado= 'Obtenidos'
        else:
            estado= 'Sin obtener'
            
        info.append({
            'palabra': word_name,
            'cantidad': count,
            'estado': estado,
        })
                
    return render(request, 'getting_keypoints.html', {
        'user': request.user,
        'info': info
    })
    
class training_model_view(LoginRequiredMixin,ListView):   
    model = Words_state
    template_name = 'training_model.html'
    paginate_by= 3
    context_object_name = 'data'
    login_url = '/'
    
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

