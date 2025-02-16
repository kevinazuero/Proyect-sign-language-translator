import os
from core.models import Words_state
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from core.training.training_model import training_model
from core.utils.constants import MODEL_NAME
from keras import backend as k
from django.shortcuts import redirect


class TrainingModelView(LoginRequiredMixin,ListView):
    model = Words_state
    template_name = 'training_model.html'
    paginate_by= 3
    context_object_name = 'data'
    login_url = '/'


def training_all_model(request):
    root = os.getcwd()
    data_path = os.path.join(root, "data")
    save_path = os.path.join(root, "models")
    model_path = os.path.join(save_path, MODEL_NAME)

    if os.path.exists(model_path):
        print(f"El modelo ya existe en: {model_path}. Eliminando...")
        os.remove(model_path)
    k.clear_session()
    training_model(data_path, model_path)
    Words_state.objects.all().update(state=True)
    return redirect('core:Entrenamiento_modelo')