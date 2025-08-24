# camera_test.py
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import cv2
import torch
import time
import os
import socket
from datetime import datetime
import csv
import threading

# ---------------- Config ----------------
VIDEO_SOURCE = 'http://172.20.10.5:8080/video'   # Your phone IP camera stream
CSV_FILE = 'detections.csv'
SNAPSHOT_DIR = 'snapshots'
GPS_PORT = 5055
CONFIDENCE_THRESHOLD = 0.50  # 🔻 Updated from 0.90 to 0.70
CAPTURE_INTERVAL = 20  # seconds

# Create snapshots folder
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# ---------------- GPS Listener ----------------
gps_data = {'lat': None, 'lon': None}

def receive_gps():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', GPS_PORT))
    print(f"Listening for GPS data on port {GPS_PORT}...")
    while True:
        data, _ = s.recvfrom(1024)
        try:
            lat, lon = data.decode().split(',')
            gps_data['lat'] = float(lat)
            gps_data['lon'] = float(lon)
        except:
            continue

threading.Thread(target=receive_gps, daemon=True).start()

# ---------------- Detection Model ----------------
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.classes = [0]  # Only person class

# ---------------- CSV Setup ----------------
if not os.path.isfile(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Label', 'Confidence', 'Latitude', 'Longitude', 'Image'])

# ---------------- Camera Loop ----------------
cap = cv2.VideoCapture(VIDEO_SOURCE)
last_capture_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    results = model(frame)
    for *box, conf, cls in results.xyxy[0].tolist():
        label = model.names[int(cls)]
        if label == 'person' and conf >= CONFIDENCE_THRESHOLD:
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            current_time = time.time()
            if current_time - last_capture_time >= CAPTURE_INTERVAL:
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                img_filename = os.path.join(SNAPSHOT_DIR, f'snapshot_{timestamp}.jpg')
                cv2.imwrite(img_filename, frame)

                latitude = gps_data['lat'] if gps_data['lat'] is not None else "N/A"
                longitude = gps_data['lon'] if gps_data['lon'] is not None else "N/A"

                with open(CSV_FILE, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        label, f"{conf:.2f}", latitude, longitude, img_filename
                    ])

                print(f"📸 Snapshot saved: {img_filename}")
                last_capture_time = current_time

    cv2.imshow("Live Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
