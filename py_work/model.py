import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

def build_model(input_shape, output_shape):
    model = Sequential([
        Dense(24, input_shape=(input_shape,), activation='relu'),
        Dense(24, activation='relu'),
        Dense(output_shape, activation='linear')
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    return model
