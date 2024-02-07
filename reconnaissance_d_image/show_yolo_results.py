from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')
def process_video( input_video_path, output_video_path, display=True, model='yolov8n.pt'):
        # Open the input video
        cap = cv2.VideoCapture(input_video_path)
        model = YOLO(model)
        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 format
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

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

        # Release everything when done
        cap.release()
        out.release()
        cv2.destroyAllWindows()

# Usage example
input_video_path = '../Dataset/CarCrash/videos/Crash-1500/000293.mp4'
output_video_path = '../Dataset/CarCrash/videos/detected_video/crash_000293.mp4'

process_video(input_video_path, output_video_path, display=True)