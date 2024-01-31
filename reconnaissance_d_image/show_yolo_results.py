from ultralytics import YOLO
import cv2



class YOLO_Results() : 
    def __init__(self, video_path="../Dataset/CarCrash/videos/Normal/000100.mp4",output_video_path="../Dataset/CarCrash/videos/detected_video/000100.mp4",model = 'yolov8n.pt'):
        self.model = YOLO(model)
        self.cap = cv2.VideoCapture(video_path)
        self.video_path=video_path
        self.output_video_path=output_video_path
    
    def process_video( self, display=True):
        # Open the input video
        cap = cv2.VideoCapture(self.input_video_path)

        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 format
        out = cv2.VideoWriter(self.output_video_path, fourcc, fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Your existing object detection and bounding box drawing code
            results = model.track(frame, persist=True)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()
            # Write the frame with bounding boxes to output video
            out.write(annotated_frame)

            # Optionally display the frame (comment out if not needed)
            if display:
                cv2.imshow('Frame', annotated_frame)

                # Exit on pressing 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
if __name__=="__main__":
    model=YOLO_Results()
    model.show_results()