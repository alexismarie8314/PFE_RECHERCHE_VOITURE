import cv2
import numpy as np
import os


class model_testing:
    
    def __init__(self, model_weights="YOLO/yolov4.weights", model_config="YOLO/yolov4.cfg", video_path="../Dataset/CarCrash/videos/Normal/000100.mp4"):  
        #verifier si le fichier des poids existe :
        if  not os.path.isfile("YOLO/yolov4.weights"):
            print("Le fichier des poids n'existe pas !")
            #   wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
            print("Téléchargement des poids...")
            os.system("wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights")
            
        if not os.path.isfile("YOLO/yolov4.cfg"):
            print("Le fichier de configuration n'existe pas !")
            #   wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg
            print("Téléchargement du fichier de configuration...")
            os.system("wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg")
        
        if not os.path.isfile("YOLO/coco.names"):
            print("Le fichier des classes n'existe pas !")
            #   wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/coco.names
            print("Téléchargement du fichier des classes...")
            os.system("wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/coco.names")
            
        
        self.net=cv2.dnn.readNet(model_config, model_weights)
        
        self.video=cv2.VideoCapture(video_path)
        
        with open('YOLO/coco.names', 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        
    def detect_object(self):
        while self.video.isOpened():
            ret, frame = self.video.read()
            if not ret:
                break

            height, width, _ = frame.shape

            # Convertir la frame en blob
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)

            # Obtenir les détections de YOLO
            layer_names = self.net.getLayerNames()
            output_layer_indexes = self.net.getUnconnectedOutLayers().flatten()
            output_layers = [layer_names[i - 1] for i in output_layer_indexes]

            outs = self.net.forward(output_layers)

            # Afficher les informations sur les objets détectés
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        # Calculer les coordonnées de la boîte englobante
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Dessiner la boîte englobante
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        cv2.putText(frame, self.classes[class_id], (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)

            # Afficher la frame
            cv2.imshow('Frame', frame)

            # Arrêter si 'q' est pressé
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.video.release()
        cv2.destroyAllWindows()

if __name__=="__main__":
    model=model_testing()
    model.detect_object()
    print("Done!")
                