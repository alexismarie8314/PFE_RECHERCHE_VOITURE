import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Reshape, SimpleRNN, Dense, TimeDistributed, Flatten


class accident_anticipation_model():
    
    def __init__(self):
        self.model=self.build_model()
        
    def build_model(self):
        # Créer le modèle
        model = Sequential()

        # Ajouter des couches Conv2D et MaxPooling2D
        # Remarque : Tu dois choisir le nombre et la taille des filtres en fonction de tes données
        # Première couche Conv2D et MaxPooling2D
        model.add(TimeDistributed(Conv2D(32, (3, 3), activation='relu', padding='same'), input_shape=(30, 19, 6, 1)))
        model.add(TimeDistributed(MaxPooling2D(2, 2)))

        # Deuxième couche Conv2D avec un filtre plus petit ou padding
        model.add(TimeDistributed(Conv2D(64, (2, 2), activation='relu', padding='same'))) # J'ai modifié la taille du filtre et ajouté le padding
        model.add(TimeDistributed(MaxPooling2D(2, 2)))

        model.add(TimeDistributed(Flatten()))

        # Reshape pour le RNN
        model.add(Reshape((30, -1)))  # -1 signifie que cette dimension sera calculée automatiquement

        # Ajouter des couches RNN
        model.add(SimpleRNN(50, activation='relu', return_sequences=True))
        model.add(SimpleRNN(50, activation='relu'))

        # Couche de sortie
        model.add(Dense(2, activation='softmax')) 

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        print(model.summary())
        return model

if __name__=="__main__":
    print(accident_anticipation_model().model.summary())