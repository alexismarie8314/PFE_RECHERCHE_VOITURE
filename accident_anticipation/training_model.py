import pandas as pd
import numpy as np
from data_preparation import prepare_data
from model_build import accident_anticipation_model

#Retriving the data :   

X_train,X_test,y_train,y_test=prepare_data(1000).get_X_train(),prepare_data(1000).get_X_test(),prepare_data(1000).get_y_train(),prepare_data(1000).get_y_test()

model=accident_anticipation_model().model

model.fit(X_train,y_train,epochs=10,validation_data=(X_test,y_test))