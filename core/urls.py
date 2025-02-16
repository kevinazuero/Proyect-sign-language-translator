from django.urls import path
from core.views import edit, register, log_out, ListHistory, delete_history, \
    ClearHistory, save_word, mostrar_html, text_speech, menu_training_view, \
    training_view, get_keypoint, delete_keypoint, getting_keypoint_view, delete_word, training_all_model, \
    TrainingModelView
from core.views.running_camera import capture_samples,translator_camera

app_name = "core"
urlpatterns = []

#urls for account
urlpatterns += [
    path('editar/', edit.edit_user, name='editar'),
    path('registrar/', register, name='registrar'),
    path('salir/', log_out, name='salir'),
]
#urls for history
urlpatterns += [
    path('historial/', ListHistory.as_view(), name='historial'),
    path('historial/delete/<int:pk>/', delete_history, name='historial_delete'),
    path('historial/clear/', ClearHistory.as_view(), name='clear_historial'),
    path('historial/save_word', save_word, name='save_word'),
]
#urls for home
urlpatterns += [
    path('inicio/', mostrar_html, name='inicio'),
    path('text_speech', text_speech, name='text_speech'),
]
#urls for translator
urlpatterns += [
    path('video_feed', translator_camera.video_feed, name='video_feed'),
    path('start_camera', translator_camera.start_camera, name='start_camera'),
    path('stop_camera', translator_camera.stop_camera, name='stop_camera'),
]
#urls for training
urlpatterns += [
    path('menu_entrenamiento/', menu_training_view, name='menu_entrenamiento'),
]
#urls for capture samples
urlpatterns += [
    path('entrenamiento/', training_view, name='entrenamiento'),
    path('entrenamiento/video_feed', capture_samples.video_feed, name='training_word'),
    path('entrenamiento/start_camera', capture_samples.start_camera, name='starting_training_word'),
    path('entrenamiento/stop_camera', capture_samples.stop_camera, name='stoping_training_word'),
    path('entrenamiento/get_progress', capture_samples.get_progress, name='get_progress_training'),
]
#urls for keypoints
urlpatterns += [
    path('obtencion_puntos_clave/', getting_keypoint_view, name='obtencion_puntos_clave'),
    path('entrenamiento/get_keypoints', get_keypoint, name='get_keypoints'),
    path('eliminar/<str:palabra>/', delete_word,  name='eliminar_palabra'),
]
#urls for training model
urlpatterns += [
    path('eliminar_keypoint/<str:palabra>/', delete_keypoint, name='eliminar_keypoint'),
    path('Entrenamiento_modelo/', TrainingModelView.as_view(), name='Entrenamiento_modelo'),
    path('entrenamiento/training_model',training_all_model, name='training_model'),
]