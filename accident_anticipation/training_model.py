import pandas as pd
import numpy as np
from data_preparation import prepare_data
from model_build import accident_anticipation_model
#on va utiliser tensorboard pôur monitorer l'entrainement
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard
import datetime

#tensorboard --logdir logs/fit

log_dir="logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

#Retriving the data :   

X_train,X_test,y_train,y_test=prepare_data().get_X_train(),prepare_data().get_X_test(),prepare_data().get_y_train(),prepare_data().get_y_test()

print(X_train.shape,X_test.shape,y_train.shape,y_test.shape)
model=accident_anticipation_model().model

model.fit(X_train,y_train,epochs=50,batch_size=32, validation_data=(X_test,y_test),callbacks=[TensorBoard(log_dir=log_dir, histogram_freq=1)])