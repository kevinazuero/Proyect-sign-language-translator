from keras.models import Sequential
from keras.layers import LSTM, Dense
from .constants import LENGTH_KEYPOINTS, MAX_LENGTH_FRAMES
from keras.layers import Dropout
from keras.optimizers import Adam
from keras.layers import BatchNormalization



NUM_EPOCH = 120

def get_model(output_length: int):
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, activation='tanh', input_shape=(MAX_LENGTH_FRAMES, LENGTH_KEYPOINTS)))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(LSTM(128, return_sequences=False, activation='tanh'))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(Dense(128, activation='linear'))
    model.add(Dropout(0.2))
    model.add(Dense(output_length, activation='softmax'))
    model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])
    return model




# def get_model(output_length: int):
#     model = Sequential()
#     model.add(LSTM(128, return_sequences=True, activation='relu', input_shape=(MAX_LENGTH_FRAMES, LENGTH_KEYPOINTS)))
#     model.add(Dropout(0.3))
#     model.add(LSTM(256, return_sequences=False, activation='relu'))
#     model.add(Dropout(0.3))
#     model.add(Dense(128, activation='relu'))
#     model.add(Dropout(0.3))
#     model.add(Dense(output_length, activation='softmax'))
#     model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])
#     return model

# def get_model(output_lenght: int):
#     model = Sequential()
#     model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(MAX_LENGTH_FRAMES, LENGTH_KEYPOINTS)))
#     model.add(LSTM(128, return_sequences=True, activation='relu'))
#     model.add(LSTM(128, return_sequences=False, activation='relu'))
#     model.add(Dense(64, activation='relu'))
#     model.add(Dense(64, activation='relu'))
#     model.add(Dense(32, activation='relu'))
#     model.add(Dense(32, activation='relu'))
#     model.add(Dense(output_lenght, activation='softmax'))
#     model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
#     return model