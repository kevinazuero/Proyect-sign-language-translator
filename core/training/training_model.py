import numpy as np
from core.utils.model import NUM_EPOCH, get_model
from keras import preprocessing
from keras import utils
from core.utils.helpers import get_actions, get_sequences_and_labels
from core.utils.constants import MAX_LENGTH_FRAMES
from keras.callbacks import ReduceLROnPlateau, EarlyStopping, TensorBoard


def training_model(data_path, model_path):
    actions = get_actions(data_path) # ['word1', 'word2', 'word3]
    
    sequences, labels = get_sequences_and_labels(actions, data_path)
    
    sequences = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_LENGTH_FRAMES,padding='post', truncating='post', dtype='float32')

    X = np.array(sequences)
    y = utils.to_categorical(labels).astype(int)
    
    model = get_model(len(actions))

    validation_split = 0.2
    
    # callbacks changes
    lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6)
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    tensorboard = TensorBoard(log_dir='./logs')
    
    

    model.fit(X, y, epochs=NUM_EPOCH, validation_split=validation_split, callbacks=[lr_scheduler, early_stopping, tensorboard])
    model.summary()
    model.save(model_path)

# if __name__ == "__main__":
#     root = os.getcwd()
#     data_path = os.path.join(root, "data")
#     actions = get_actions(data_path)  # ['word1', 'word2', 'word3']
#     save_path = os.path.join(root, "models")
#     model_path = os.path.join(save_path, MODEL_NAME)
    
#     # Verificar si el archivo o directorio del modelo existe
#     if os.path.exists(model_path):
#         print(f"El modelo ya existe en: {model_path}. Eliminando...")
#         os.remove(model_path)  # Eliminar archivo
            
#     training_model(data_path, model_path)   
    
    # root = os.getcwd()
    # data_path = os.path.join(root, "data")
    # actions = get_actions(data_path) # ['word1', 'word2', 'word3]
    # save_path = os.path.join(root, "models")
    # model_path = os.path.join(save_path, MODEL_NAME)
    
    # training_model(data_path, model_path)
    