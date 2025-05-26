# 🛞 Rover Vision-Control Project (Raspberry Pi + YOLO + Gesture Control)

This project enables real-time control of a ground rover using hand gestures and object/person tracking via computer vision. The system follows a **client-server architecture** optimized for Raspberry Pi Zero 2W.

---

## 🚦 Project Overview

- **Client (Raspberry Pi Zero 2W)**: Captures camera feed and sends frames over WebSocket.
- **Server (MacBook or PC)**: Performs gesture detection, object/person tracking, and sends back movement commands.
- **Communication**: Lightweight WebSocket protocol over local Wi-Fi.

---

## 🧠 Functional Modes

| Mode               | Trigger Gesture       | Description                                    |
|--------------------|------------------------|------------------------------------------------|
| Idle Mode          | No gesture detected    | Rover stops and awaits input                  |
| Hand Tracking Mode | Open palm (🖐️)         | Tracks hand movement to control direction     |
| Command Mode       | Thumbs-up, peace, etc. | Executes predefined commands (e.g., stop)     |
| Person Tracking    | Pointing gesture       | Tracks selected person from YOLO detection    |

---

## 🖥️ Server-Side (MacBook/PC)

### 🔧 Responsibilities
- Run YOLO (hand/person detection)
- Run gesture recognition (MediaPipe or custom CNN)
- FSM-based control logic (mode switching)
- Send commands to client over WebSocket

### 🛠️ Tools & Libraries
- Python 3.10+
- OpenCV
- YOLOv8 (Ultralytics)
- MediaPipe or custom hand gesture model
- WebSocket server: `websockets` or `FastAPI + WebSocket`

---

## 🍓 Client-Side (Raspberry Pi Zero 2W)

### 🔧 Responsibilities
- Capture camera feed (PiCamera/OpenCV)
- Compress and transmit frames to server
- Receive motor commands (JSON)
- Drive GPIO-controlled motors

### 🛠️ Tools & Libraries
- Python 3.9+ (Lite OS)
- `opencv-python` (use headless version)
- `websockets` or `websocket-client`
- `RPi.GPIO` or `gpiozero`

---

## 🗂️ Suggested File Structure
```
rover_project/
├── client/ # Code for Raspberry Pi
│ ├── camera_streamer.py # Captures video and sends frames
│ ├── motor_controller.py # Executes commands via GPIO
│ ├── client_main.py # WebSocket client loop
│ └── utils/ # Frame compression, logging
├── server/ # Code for YOLO and control logic
│ ├── gesture_detector.py # Detects hand gestures
│ ├── object_tracker.py # Person/hand tracking module
│ ├── fsm_controller.py # FSM mode switch logic
│ ├── server_main.py # WebSocket server loop
│ └── models/ # Pretrained YOLO or CNN weights
├── README.md # Project documentation
└── requirements.txt # Shared dependencies
```


---

## ✅ Next Steps

- [ ] Implement YOLO + gesture detector (server side)
- [ ] Setup camera and WebSocket communication (client side)
- [ ] Build FSM controller (hand → command → GPIO)
- [ ] Test latency and optimize image transmission
- [ ] Expand modes: person-follow, auto-stop on lost signal, etc.

---

## 📌 Notes

- Raspberry Pi Zero 2W lacks GPU, hence no onboard vision processing
- Real-time inference is handled entirely by the server
- System designed to run over low-latency Wi-Fi or local hotspot

---

## 🔗 References

- YOLOv8: https://docs.ultralytics.com/
- MediaPipe Hands: https://google.github.io/mediapipe/solutions/hands
- FastAPI WebSocket: https://fastapi.tiangolo.com/advanced/websockets/


## Architecture

```
 ┌─────────────────────────────┐
 │       FastAPI Client        │ (Health Check, Manual Triggers)
 └─────────────────────────────┘
             │
             ▼
 ┌─────────────────────────────┐
 │     CommunicationManager    │ <-- Singleton (handles all WebSocket I/O)
 └─────────────────────────────┘
         ▲               ▲
         │               │
 ┌──────────────┐   ┌──────────────┐
 │   Sensor     │   │   Executor   │
 │  Modules     │   │   Modules    │
 │ (Camera etc) │   │ (Motor etc)  │
 └──────────────┘   └──────────────┘

```


## Folder Structure

```
rover_client/
│
├── rover_client.py              # 🚀 FastAPI entry point and orchestrator
├── config.yaml                  # ⚙️  Global config (URIs, flags, etc.)
├── communication_manager.py     # 🔁 Singleton for all WebSocket I/O and routing
│
├── sensors/
│   ├── sensor.py                # 📡 Abstract base class for all sensors
│   └── camera_sensor.py         # 📷 Captures frames and streams via CommunicationManager
│
├── controllers/
│   ├── controller.py            # 🎮 Base class for executors
│   └── motor_controller.py      # ⚙️  Executes motor commands (includes low-level GPIO ops)
│
├── utils.py                     # 🧰 Shared utilities (logging, config loading, etc.)
```
