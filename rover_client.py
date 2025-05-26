# rover_client.py

import asyncio
import yaml
from fastapi import FastAPI
import uvicorn

from utils import get_logger
from communication_manager import CommunicationManager
from sensors.camera_sensor import CameraSensor
from controllers.motor_controller import MotorController

logger = get_logger("RoverClient", console=True)
# --- Load Config ---
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

SERVER_URI = config.get("server_uri")

# --- FastAPI App ---
app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    comm = CommunicationManager.get_instance(SERVER_URI)

    # Register sensors and controllers
    comm.register_sensor(CameraSensor())
    comm.register_controller(MotorController())

    logger.info("Registered Sensor : [CameraSensor]")
    logger.info("Registered Controller : [MotorController]")
    await comm.start_all()
    

@app.on_event("shutdown")
async def shutdown_event():
    comm.clean_all()

# --- Run App ---
if __name__ == "__main__":
    uvicorn.run("rover_client:app", host="0.0.0.0", port=5000, reload=False)
