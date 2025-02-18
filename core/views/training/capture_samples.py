from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from core.utils.constants import ROOT_PATH, FRAME_ACTIONS_PATH
from core.utils.helpers import get_actions, delete_files
import os


@login_required
def training_view(request):
    root = os.getcwd()
    data_path = os.path.join(root, "data")
    actions = get_actions(data_path)
    return render(request, 'training.html', {
        'user': request.user,
        'actions':actions,
    })

def delete_word(request, palabra):
    if request.method == "POST":
        try:
            words_path = os.path.join(ROOT_PATH, FRAME_ACTIONS_PATH)
            delete_files(palabra,words_path)
            return redirect('core:obtencion_puntos_clave')
        except Exception as e:
            return HttpResponse(f"Error al eliminar la palabra: {e}", status=500)
    else:
        return HttpResponse("Método no permitido", status=405)