import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.utils.helpers import get_actions
from core.utils.helpers import count_samples
from core.utils.helpers import delete_files
from core.utils.constants import FRAME_ACTIONS_PATH, ROOT_PATH, DATA_PATH, MODEL_NAME
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from core.training.create_keypoints import create_keypoints
from core.models import Words_state

@login_required
def getting_keypoint_view(request):
    root = os.getcwd()
    data_path = os.path.join(root, "data")
    actions = get_actions(data_path)
    words_path = os.path.join(ROOT_PATH, FRAME_ACTIONS_PATH)
    info = []

    for word_name in os.listdir(words_path):
        count = count_samples(word_name)
        if word_name in actions:
            estado = 'Obtenidos'
        else:
            estado = 'Sin obtener'

        info.append({
            'palabra': word_name,
            'cantidad': count,
            'estado': estado,
        })

    return render(request, 'getting_keypoints.html', {
        'user': request.user,
        'info': info
    })


def delete_keypoint(request, palabra):
    if request.method == "POST":
        try:
            words_path = DATA_PATH
            delete_files(palabra, words_path)

            word_state = get_object_or_404(Words_state, word=palabra)
            word_state.delete()
            return redirect('core:Entrenamiento_modelo')
        except Exception as e:
            return HttpResponse(f"Error al eliminar la palabra: {e}", status=500)
    else:
        return HttpResponse("Método no permitido", status=405)


def get_keypoint(request):
    words_path = os.path.join(ROOT_PATH, FRAME_ACTIONS_PATH)

    os.makedirs(DATA_PATH, exist_ok=True)

    for word_name in os.listdir(words_path):
        word_path = os.path.join(words_path, word_name)
        hdf_path = os.path.join(DATA_PATH, f"{word_name}.h5")
        word_with_h5 = f"{word_name}.h5"

        if not os.path.exists(hdf_path):
            print(f'Creando keypoints de "{word_name}"...')
            create_keypoints(word_path, hdf_path)
            Words_state.objects.create(word=word_with_h5)
            print(f"Keypoints creados!")
        else:
            print(f'Se omitió "{word_name}" porque los keypoints ya existen.')
    return JsonResponse({"message": "se han creado los keypoints"})