🚁 UAV-Based Disaster Response using YOLO & GPS Tracking
📌 Overview

This project integrates Unmanned Aerial Vehicles (UAVs) with real-time person detection using the YOLO deep learning model, GPS tagging, and a dashboard interface for disaster response scenarios.
The system helps in:

Detecting stranded humans during disasters (floods, earthquakes, landslides, etc.).

Tagging their geolocation (latitude & longitude).

Logging detections with images + coordinates in a structured format.

Displaying results on an interactive map for rescue operations.

✨ Features

YOLOv5/YOLOv8 Model for real-time person detection.

GPS Integration: Receives live GPS coordinates from the UAV/phone via UDP.

Snapshot Capture: Saves images when detection probability > threshold (default: 70%).

CSV Logging: Records timestamp, label, confidence, GPS location, and image path.

Interactive Dashboard (Streamlit + Folium):

Live detection feed.

Map with clickable detection points.

Option to send location info to rescue teams/drones.

Swarm Communication Ready: Built with delay-tolerant networking concepts for multi-UAV coordination.

🏗️ System Architecture

UAV Camera Feed → Captured using phone/drone camera (IP webcam).

YOLO Model → Detects persons in real-time from video frames.

GPS Module → Fetches latitude & longitude from UAV.

CSV Logging → Stores detection data for post-analysis.

Dashboard → Displays detections + live map with Folium.

⚙️ Installation
1. Clone Repo
git clone https://github.com/your-username/uav-disaster-response.git
cd uav-disaster-response

2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate   # On Linux/Mac

3. Install Dependencies
pip install -r requirements.txt


requirements.txt

torch
torchvision
opencv-python
pandas
streamlit
folium
ultralytics

▶️ Usage
Run Person Detection + GPS Logging
python camera_test.py

Run Dashboard Interface
streamlit run dashboard_ui.py

📊 Example Output

Snapshots: Saved in /snapshots folder.

detections.csv:

Timestamp	Label	Confidence	Latitude	Longitude	Image Path
2025-08-20 14:12:01	Person	0.85	12.9716	77.5946	snapshots/img1.jpg

Dashboard Map (Folium): Click on detection → Opens Google Maps.

🌍 Applications

Disaster response (earthquake, flood, landslide).

Military surveillance.

Wildlife monitoring.

Search & rescue operations.

🚀 Future Scope

Multi-UAV Swarm Optimization (PSO, ACO).

Integration with DTN (Delay-Tolerant Networks).

Satellite data fusion for large-scale monitoring.

AI-powered decision-making for autonomous UAV response.

📚 References

Redmon, J., et al. You Only Look Once (YOLO), CVPR, 2016.

Bochkovskiy, A., et al. YOLOv4: Optimal Speed and Accuracy of Object Detection, arXiv, 2020.

Qu, Y., et al. Swarm Intelligence-Based UAV Coordination in Disaster Relief, Sensors, 2020.

Ultralytics, YOLOv5 Documentation, 2025.

Streamlit Docs, Interactive Dashboards, 2025.
