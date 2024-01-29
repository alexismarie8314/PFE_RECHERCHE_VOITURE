from ultralytics import YOLO
import cv2



class YOLO_Results() : 
    def __init__(self, video_path="../Dataset/CarCrash/videos/Normal/000100.mp4",model = 'yolov8n.pt'):
        self.model = YOLO(model)
        self.cap = cv2.VideoCapture(video_path)
    
    def show_results(self):
        # Loop through the video frames
            while self.cap.isOpened():
                # Read a frame from the video
                success, frame = self.cap.read()

                if success:
                    # Run YOLOv8 tracking on the frame, persisting tracks between frames
                    results = self.model.track(frame, persist=True)

                    # Visualize the results on the frame
                    annotated_frame = results[0].plot()

                    # Display the annotated frame
                    cv2.imshow("YOLOv8 Tracking", annotated_frame)

                    # Break the loop if 'q' is pressed
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                else:
                    # Break the loop if the end of the video is reached
                    break

            # Release the video capture object and close the display window
            self.cap.release()
            cv2.destroyAllWindows()
            
if __name__=="__main__":
    model=YOLO_Results()
    model.show_results()