import os
import yaml
import json
import shutil
import pandas as pd
from sklearn.model_selection import train_test_split


class COCO2YOLO:
    def __init__(self, dataset_path, output_path):
        self.dataset_path = dataset_path
        self.output_path = output_path
        self.class_names = self.read_class_names()

    def read_class_names(self):
        # Assuming class names are in the same order as the categories in the annotations
        with open(os.path.join(self.dataset_path, 'test.json'), 'r') as file:
            data = json.load(file)
        categories = data['categories']
        class_names = {category['id']: category['name'] for category in categories}
        return class_names

    def convert_annotations(self, json_file):
        # Read JSON file
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        for img in data['images']:
            # Get image information
            image_id = img['id']
            file_name = os.path.splitext(img['file_name'])[0]  # without file extension
            width = img['width']
            height = img['height']

            # Filter annotations for the current image
            annotations = [a for a in data['annotations'] if a['image_id'] == image_id]

            # Prepare YOLO annotations
            yolo_annotations = []
            for ann in annotations:
                # Convert COCO bbox to YOLO format
                x_center = (ann['bbox'][0] + ann['bbox'][2] / 2) / width
                y_center = (ann['bbox'][1] + ann['bbox'][3] / 2) / height
                w = ann['bbox'][2] / width
                h = ann['bbox'][3] / height
                # Adjust for 0-indexing
                class_id = ann['category_id'] - 1
                yolo_annotations.append(f"{class_id} {x_center} {y_center} {w} {h}")

            # Write annotations to file
            txt_file_path = os.path.join(self.output_path, f"{file_name}.txt")
            with open(txt_file_path, 'w') as txt_file:
                txt_file.write('\n'.join(yolo_annotations))
    def generate_yolo_config(self):
        # Define dataset structure
        data_config = {
            'path': self.output_path,  # dataset root dir
            'train': 'images/train2017',  # train images (relative to 'path')
            'val': 'images/val2017',  # val images (relative to 'path')
            'test': 'images/test2017',  # test images (optional)
            'names': self.class_names
        }

        # Write the YAML dataset config file
        config_path = os.path.join(self.output_path, 'dataset_config.yaml')
        with open(config_path, 'w') as file:
            yaml.dump(data_config, file, default_flow_style=False)
        return config_path

    def organize_dataset(self, config_path):
        # Read the config to get the paths
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        # Create directories
        for key in ['train', 'val', 'test']:
            dir_path = os.path.join(self.output_path, config[key])
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

        df=pd.DataFrame(columns=['image_name','label_file_name','id'])
        for elt in os.listdir(self.output_path):
            if elt.endswith('.jpg'):
                if not os.path.exists(os.path.join(self.output_path,elt.replace('.jpg','.txt'))):
                    pass
                if os.path.exists(os.path.join(self.output_path,elt.replace('.jpg','.txt'))):
                    df.loc[len(df.index)] = [elt,elt.replace('.jpg','.txt'),elt.replace('.jpg','')]

        train, test = train_test_split(df, test_size=0.2)
        val, test = train_test_split(test, test_size=0.5)
        for index, row in train.iterrows():
            shutil.move(os.path.join(self.output_path,row['image_name']),os.path.join(self.output_path,'images/train2017'),copy_function=shutil.copy2)
            shutil.move(os.path.join(self.output_path,row['label_file_name']),os.path.join(self.output_path,'images/train2017'),copy_function=shutil.copy2)
        for index, row in val.iterrows():
            shutil.move(os.path.join(self.output_path,row['image_name']),os.path.join(self.output_path,'images/val2017'),copy_function=shutil.copy2)
            shutil.move(os.path.join(self.output_path,row['label_file_name']),os.path.join(self.output_path,'images/val2017'),copy_function=shutil.copy2)
        for index, row in test.iterrows():
            shutil.move(os.path.join(self.output_path,row['image_name']),os.path.join(self.output_path,'images/test2017'),copy_function=shutil.copy2)
            shutil.move(os.path.join(self.output_path,row['label_file_name']),os.path.join(self.output_path,'images/test2017'),copy_function=shutil.copy2)

    def test_YOLOY_txt_file_before_moving(self):
        count=0
        for elt in os.listdir(self.output_path):
            
            if elt.endswith('.jpg'):
                img_id=elt.replace('.jpg','')
                if not os.path.exists(os.path.join(self.output_path,img_id+'.txt')):
                    count+=1
        print(str(count)+' errors')
    def test_each_pic_has_txt(self):
       # """ verifier que chaque image des dossier trai2017,val2017,test2017 a un fichier txt correspondant """
        cnt=0
        for elt in os.listdir(os.path.join(self.output_path,'images/train2017')):
            if elt.endswith('.jpg'):
                if not os.path.exists(os.path.join(self.output_path,'images/train2017',elt.replace('.jpg','.txt'))):
                    print('error, no txt file for image '+elt)
                    cnt+=1
        for elt in os.listdir(os.path.join(self.output_path,'images/val2017')):
            if elt.endswith('.jpg'):
                if not os.path.exists(os.path.join(self.output_path,'images/val2017',elt.replace('.jpg','.txt'))):
                    print('error, no txt file for image '+elt)
                    cnt+=1
        for elt in os.listdir(os.path.join(self.output_path,'images/test2017')):
            if elt.endswith('.jpg'):
                if not os.path.exists(os.path.join(self.output_path,'images/test2017',elt.replace('.jpg','.txt'))):
                    print('error, no txt file for image '+elt)
                    cnt+=1
        if cnt==0:
            print('no error')
        
    def test_each_txt_has_pic(self):
        """ verifier que chaque txt des dossier trai2017,val2017,test2017 a une image correspondante """
        cnt=0
        for elt in os.listdir(os.path.join(self.output_path,'images/train2017')):
            if elt.endswith('.txt'):
                if not os.path.exists(os.path.join(self.output_path,'images/train2017',elt.replace('.txt','.jpg'))):
                    print('error, no jpg file for txt '+elt)
                    cnt+=1
        for elt in os.listdir(os.path.join(self.output_path,'images/val2017')):
            if elt.endswith('.txt'):
                if not os.path.exists(os.path.join(self.output_path,'images/val2017',elt.replace('.txt','.jpg'))):
                    print('error, no jpg file for txt '+elt)
                    cnt+=1
        for elt in os.listdir(os.path.join(self.output_path,'images/test2017')):
            if elt.endswith('.txt'):
                if not os.path.exists(os.path.join(self.output_path,'images/test2017',elt.replace('.txt','.jpg'))):
                    print('error, no jpg file for txt '+elt)
                    cnt+=1
        if cnt==0:
            print('no error')
            
if __name__==   "__main__":
    dataset_path = '../Dataset/DFG_traffic_signal/DFG-tsd-aug-annot-json'  # The path to the directory containing train.json and test.json
    output_path = '/Users/lucabankofski/Documents_local/PFE_RECHERCHE_VOITURE/Dataset/DFG_traffic_signal/JPEGImages'  # The directory to save YOLO annotations and config

    # Create an instance of the class
    coco2yolo = COCO2YOLO(dataset_path, output_path)

    # Convert annotations for training and testing
    coco2yolo.convert_annotations(os.path.join(dataset_path, 'train.json'))
    coco2yolo.convert_annotations(os.path.join(dataset_path, 'test.json'))
    coco2yolo.test_YOLOY_txt_file_before_moving()
    config_path = coco2yolo.generate_yolo_config()
    coco2yolo.organize_dataset(config_path)
    coco2yolo.test_each_pic_has_txt()
    coco2yolo.test_each_txt_has_pic()
    print(f"YOLO formatted annotations are saved in: {output_path}")
    print("number of class is ", len(list(coco2yolo.class_names)))