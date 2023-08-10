import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('best.pt')
video_path = "test-vid.mp4"
cap = cv2.VideoCapture(video_path)
#Initialize output video
output = intialize_output()

# Loop through the video frames
while cap.isOpened():
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, conf=0.6, iou=0.6, device='mps')
        annotated_frame = annotate_frame(results,frame)
        output.write_frame(annotated_frame)
    else:
        # Break the loop if the end of the video is reached
        break

cap.release()
cv2.destroyAllWindows()
