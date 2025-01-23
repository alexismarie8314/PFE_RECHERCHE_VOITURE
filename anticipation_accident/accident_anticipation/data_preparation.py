# Description: This file contains the code to prepare the data for training and testing

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical


class prepare_data:
    def __init__(self, number_of_items=3801,dataset_path="Dataset/CarCrash/df_for_training.parquet"):
        self.number_of_items=min(number_of_items,3801) #Number o1 items to be used for training and testing, max is 3801
        self.dataset_path=dataset_path #Path to the dataset
        
        self.data=pd.read_parquet(self.dataset_path).reset_index().iloc[:self.number_of_items]  #Read the dataset
        self.X_train,self.X_test,self.y_train,self.y_test=self.split_data() #Split the data into train and test
        
       
    def split_data(self): 
        """_summary_

        Returns:
            _type_: tuple containing X_train, X_test, y_train, y_test
        """
        X_train, X_test, y_train, y_test = train_test_split(self.data.drop(["accident_frame"],axis=1), self.data["accident_frame"], test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    def prepare_npz_file(self,file):
        """_summary_
        npz files initially contains : 
- data: Extracted 4096-dim features with shape (50, 20, 4096). It contains frame-level feature with shape (50, 1, 4096) and 19 box-level features with shape (50, 19, 4096).
- det: Detected bounding boxes with shape (50, 19, 6), where the last dim denotes (x1, y1, x2, y2, prob, cls).
- labels: One-hot video labels to indicate whether the video contains an accident, i.e., [0, 1] denotes positive (accident) and [1, 0] denotes negative (normal).
- ID: The video name for current feature file.

we decide to extract only det drom those files
        Args:
            file (__string__): feature .npz file path

        Returns:
            _type_:   array containgn the features
        """
        #Code to open and read feature in npz files
        features = np.load(file)  
        #keep only data and det from feature
        features_det = features["det"]  
   
        return features_det
    
    def extract_features(self,X):
        """ _summary_
        extract the features from the npz files

        Args:
            X (pandas series): contains the npz file names

        Returns:
            _type_: __array__ containing the features
        """
        X= np.array(X["npz_file"].apply(lambda  x : self.prepare_npz_file("Dataset/CarCrash/vgg16_features/"+ x)).to_list())
        return X
    
    def select_frames(self,X,number_of_frames=30):
        """Choose the number of frames per videos to be used for training and testing. 
        as we must detect accident before it happens, we choose by default to use the first 
        30 frames of each video

        Args:
            X (array): array containgin the features
            number_of_frames (int, optional): number of frame to be kept. Defaults to 30.

        Returns:
            array: array containg the freature with the selected frames
        """
        X=X[:,0:number_of_frames,:]
        return X
    
    def encode_y(self,y):
        """_summary_
        encode the y values to be used for training and testing

        Args:
            y (array): array containing the y values

        Returns:
            array: array containing the encoded y values
        """
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