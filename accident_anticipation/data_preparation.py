import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical


class prepare_data:
    def __init__(self, number_of_items=3801,dataset_path="Dataset/CarCrash/df_for_training.parquet"):
        self.number_of_items=min(number_of_items,3801) #Number o1 items to be used for training and testing, max is 3801
        self.dataset_path=dataset_path
        
        self.data=pd.read_parquet(self.dataset_path).reset_index().iloc[:self.number_of_items]
        self.X_train,self.X_test,self.y_train,self.y_test=self.split_data()
        
       
    def split_data(self):
        X_train, X_test, y_train, y_test = train_test_split(self.data.drop(["accident_frame"],axis=1), self.data["accident_frame"], test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    def prepare_npz_file(self,file):
        #Code to open and read feature in npz files
        features = np.load(file)  
        #keep only data and det from feature
        features_det = features["det"]  
   
        return features_det
    
    def extract_features(self,X):
        X= np.array(X["npz_file"].apply(lambda  x : self.prepare_npz_file("Dataset/CarCrash/vgg16_features/"+ x)).to_list())
        return X
    
    def select_frames(self,X,number_of_frames=30):
        X=X[:,0:number_of_frames,:]
        return X
    
    def encode_y(self,y):
        y=y.apply(lambda x : 1 if x!= -1 else 0)
        y=to_categorical(y)
        return y
    
    def get_X_train(self):
        self.X_train=self.extract_features(self.X_train)
        self.X_train=self.select_frames(self.X_train)
        return self.X_train
    
    def get_X_test(self):
        self.X_test=self.extract_features(self.X_test)
        self.X_test=self.select_frames(self.X_test)
        return self.X_test
    
    def get_y_train(self):
        self.y_train=self.encode_y(self.y_train)
        return self.y_train
    
    def get_y_test(self):
        self.y_test=self.encode_y(self.y_test)
        return self.y_test
    
    def get_all_data(self):
        return self.get_X_train(),self.get_X_test(),self.get_y_train(),self.get_y_test()
    
if __name__=="__main__":
    X_train,X_test,y_train,y_test=prepare_data().get_all_data()
    print(X_train.shape,X_test.shape,y_train.shape,y_test.shape)