from django.urls import path
from core.views import  account,historial,traductor,edit, videocamara, entrenamineto
app_name = "core"
urlpatterns = []
 
urlpatterns += [
    path('registrar/', account.register, name='registrar'),
    path('salir/', account.Salir, name='salir'), 
]

urlpatterns += [
        path('historial/', historial.list_historial.as_view(), name='historial'),
        path('historial/delete/<int:pk>/', historial.historial_delete, name='historial_delete'),
        path('historial/clear/', historial.clear_historial.as_view(), name='clear_historial'),
        path('historial/save_word', historial.save_word, name='save_word'),
]

urlpatterns += [
        path('inicio/', traductor.mostrar_html, name='inicio'),
        path('text_speech', traductor.text_speech, name='text_speech'), 
]

    
urlpatterns += [
        path('editar/', edit.edit_user, name='editar'), 
]

urlpatterns += [
    path('video_feed', videocamara.video_feed, name='video_feed'),
    path('start_camera', videocamara.start_camera, name='start_camera'),
    path('stop_camera', videocamara.stop_camera, name='stop_camera'),
]

#urls for training
urlpatterns += [
        path('menu_entrenamiento/', traductor.menu_training_view, name='menu_entrenamiento'),
        path('eliminar/<str:palabra>/', entrenamineto.eliminar_palabra, name='eliminar_palabra'),
        path('eliminar_keypoint/<str:palabra>/', entrenamineto.eliminar_keypoint, name='eliminar_keypoint'),
        path('obtencion_puntos_clave/', traductor.getting_keypoints_view, name='obtencion_puntos_clave'), 
        path('Entrenamiento_modelo/', traductor.training_model_view.as_view(), name='Entrenamiento_modelo'),  
        path('entrenamiento/', traductor.training_view, name='entrenamiento'), 
        path('entrenamiento/video_feed', entrenamineto.video_feed, name='training_word'),
        path('entrenamiento/start_camera', entrenamineto.start_camera, name='starting_training_word'),
        path('entrenamiento/stop_camera', entrenamineto.stop_camera, name='stoping_training_word'), 
        path('entrenamiento/get_progress', entrenamineto.get_progress, name='get_progress_training'), 
]

urlpatterns += [
        path('entrenamiento/get_keypoints', entrenamineto.get_keypoints, name='get_keypoints'),
        path('entrenamiento/training_model', entrenamineto.training_all_model, name='training_model'),
]