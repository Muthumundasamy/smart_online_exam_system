from ultralytics import YOLO
import cv2

# Load pretrained model (nano version for low system)
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    # Show detection
    annotated_frame = results[0].plot()
    cv2.imshow("YOLO Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()