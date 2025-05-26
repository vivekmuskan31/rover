# rover-client

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
