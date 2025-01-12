import pandas as pd
import os
import numpy as np
from core.utils.model import NUM_EPOCH, get_model
from keras import preprocessing
from keras import utils
from core.utils.helpers import get_actions, get_sequences_and_labels
from core.utils.constants import MAX_LENGTH_FRAMES, MODEL_NAME

def training_model(data_path, model_path):
    actions = get_actions(data_path) # ['word1', 'word2', 'word3]
    
    sequences, labels = get_sequences_and_labels(actions, data_path)
    
    sequences = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_LENGTH_FRAMES,padding='post', truncating='post', dtype='float32')

    X = np.array(sequences)
    y = utils.to_categorical(labels).astype(int)
    
    model = get_model(len(actions))
    model.fit(X, y, epochs=NUM_EPOCH)
    model.summary()
    model.save(model_path)

if __name__ == "__main__":
    root = os.getcwd()
    data_path = os.path.join(root, "data")
    actions = get_actions(data_path)  # ['word1', 'word2', 'word3']
    save_path = os.path.join(root, "models")
    model_path = os.path.join(save_path, MODEL_NAME)
    
    # Verificar si el archivo o directorio del modelo existe
    if os.path.exists(model_path):
        print(f"El modelo ya existe en: {model_path}. Eliminando...")
        os.remove(model_path)  # Eliminar archivo
            
    training_model(data_path, model_path)   
    
    # root = os.getcwd()
    # data_path = os.path.join(root, "data")
    # actions = get_actions(data_path) # ['word1', 'word2', 'word3]
    # save_path = os.path.join(root, "models")
    # model_path = os.path.join(save_path, MODEL_NAME)
    
    # training_model(data_path, model_path)
    