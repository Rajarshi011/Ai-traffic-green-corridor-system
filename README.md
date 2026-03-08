🚦 AI Traffic Flow Optimizer & Emergency Green Corridor System

A Smart City Traffic Management System that uses AI-based traffic analysis, adaptive traffic signals, and intelligent routing to optimize traffic flow and provide green corridors for emergency vehicles like ambulances and fire trucks.

This system simulates how a modern AI-driven urban traffic control center could dynamically manage signals and route emergency vehicles efficiently.

## 🎥 Project Demo
[![Watch the demo]
https://youtu.be/Z-6JOUA8fiI?si=MhWMcozv5cCP2xHG

📌 Features
🚗 AI Traffic Density Detection

Uses computer vision (YOLO / OpenCV) to detect vehicles.

Calculates traffic density scores.

Feeds density into the adaptive signal system.

🚦 Adaptive Traffic Signal Control

Signals automatically adjust based on traffic density.

Supports:

Adaptive AI mode

Manual signal control

🚑 Emergency Green Corridor

Finds fastest road route for ambulances/fire vehicles.

Uses OSRM routing engine.

Automatically generates green traffic corridor.

🔁 Dynamic Rerouting

Multiple routes are fetched from OSRM.

Operator can reroute ambulance manually if congestion occurs.

🗺 Interactive Smart City Map

Built using PyDeck + Mapbox visualization.

Shows:

hospitals

intersections

ambulance base

emergency routes

📊 Traffic Monitoring Dashboard

Displays:

vehicle count

density score

adaptive signal status

lane wait times

🧠 System Architecture
AI Traffic Flow Optimizer
│
├── Computer Vision
│   ├── Vehicle Detection
│   └── Traffic Density Estimation
│
├── Adaptive Signal Controller
│   ├── Density-based signal timing
│   └── Manual override system
│
├── Emergency Routing Engine
│   ├── OSRM road routing
│   └── Multi-route rerouting
│
└── Visualization Layer
    ├── Streamlit dashboard
    └── PyDeck smart city map

🗂 Project Structure

Traffic
│
├── backend
│   ├── emergency_grid.py        # City road network & routing graph
│   ├── router.py                # OSRM road routing
│   ├── signal_controller.py     # Adaptive signal algorithm
│   └── traffic_ai.py            # AI traffic detection
│
├── data
│   └── hospitals_kolkata.json
│
├── traffic.mp4                  # Traffic video for AI detection
│
├── streamlit_app.py             # Main dashboard
│
├── requirements.txt
│
└── README.md

⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/yourusername/ai-traffic-flow-optimizer.git
cd ai-traffic-flow-optimizer
2️⃣ Create virtual environment
python -m venv .venv

Activate it:

Windows

.venv\Scripts\activate

Mac/Linux

source .venv/bin/activate
3️⃣ Install dependencies
pip install -r requirements.txt
▶️ Running the Project

Start the Streamlit dashboard:

streamlit run streamlit_app.py

Open in browser:

http://localhost:8501
🖥 Dashboard Interface

The system dashboard contains:

Left Panel

AI traffic detection

vehicle count

density score

adaptive signal grid

Right Panel

emergency dispatch control

route activation

ambulance rerouting

green corridor map

🗺 Emergency Routing System

The system uses OSRM (Open Source Routing Machine) to calculate:

shortest road route

multiple alternative routes

estimated arrival time (ETA)

Routes are visualized on the map:

Color	Meaning
🟢 Green	Selected emergency route
⚪ Grey	Alternative routes
🚀 Technologies Used
Technology	Purpose
Python	Core system
Streamlit	Dashboard UI
PyDeck	Map visualization
OpenCV	Video processing
YOLO	Vehicle detection
OSRM	Road routing engine
NumPy	Data processing
🌆 Smart City Use Cases

This system can be used for:

Smart traffic control centers

Emergency vehicle routing

Urban traffic optimization

AI-based traffic signal control

Smart city infrastructure research

🧪 Future Improvements

Possible upgrades:

Live CCTV traffic feed integration

Real-time congestion detection

Ambulance tracking animation

Automatic signal preemption

GPS integration with emergency vehicles

Integration with Google Maps / OpenStreetMap APIs

👨‍💻 Author

Rajarshi Sahoo

B.Tech Computer Science & Engineering
University of Engineering and Management, Kolkata

Project Focus:
AI + Smart City Traffic Optimization

📜 License

This project is for educational and research purposes.
