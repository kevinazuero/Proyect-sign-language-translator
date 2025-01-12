import os
import pandas as pd
from mediapipe.python.solutions.holistic import Holistic
from core.utils.helpers import get_keypoints, insert_keypoints_sequence
from core.utils.constants import DATA_PATH, FRAME_ACTIONS_PATH, ROOT_PATH

def create_keypoints(frames_path, save_path):
    '''
    ### CREAR KEYPOINTS PARA UNA PALABRA
    Recorre la carpeta de frames de la palabra y guarda sus keypoints en `save_path`
    '''
    data = pd.DataFrame([])
    
    with Holistic() as model_holistic:
        for n_sample, sample_name in enumerate(os.listdir(frames_path), 1): #devuelve las carpetas dentro enumeradas
            sample_path = os.path.join(frames_path, sample_name) # ../frames_actions/hola/exanple1..2..3...4
            keypoints_sequence = get_keypoints(model_holistic, sample_path)
            data = insert_keypoints_sequence(data, n_sample, keypoints_sequence)

    data.to_hdf(save_path, key="data", mode="w")

# if __name__ == "__main__":
#     words_path = os.path.join(ROOT_PATH, FRAME_ACTIONS_PATH)
    
#     # Asegurar que el directorio de keypoints exista
#     os.makedirs(DATA_PATH, exist_ok=True)
    
#     # Generar keypoints solo para palabras nuevas
#     for word_name in os.listdir(words_path):
#         word_path = os.path.join(words_path, word_name)
#         hdf_path = os.path.join(DATA_PATH, f"{word_name}.h5")
        
#         if not os.path.exists(hdf_path):
#             print(f'Creando keypoints de "{word_name}"...')
#             create_keypoints(word_path, hdf_path)
#             print(f"Keypoints creados!")
#         else:
#             print(f'Se omitió "{word_name}" porque los keypoints ya existen.')
    
    # words_path = os.path.join(ROOT_PATH, FRAME_ACTIONS_PATH)
    
    # # GENERAR LOS KEYPOINTS DE TODAS LAS PALABRAS
    # for word_name in os.listdir(words_path):
    #     word_path = os.path.join(words_path, word_name)
    #     hdf_path = os.path.join(DATA_PATH, f"{word_name}.h5")
    #     print(f'Creando keypoints de "{word_name}"...')
    #     create_keypoints(word_path, hdf_path)
    #     print(f"Keypoints creados!")
            
    # GENERAR SOLO DE UNA PALABRA
    # word_name = "hola"
    # word_path = os.path.join(words_path, word_name)
    # hdf_path = os.path.join(data_path, f"{word_name}.h5")
    # create_keypoints(word_path, hdf_path)
    # print(f"Keypoints creados!")
