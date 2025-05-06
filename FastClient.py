import asyncio
import websockets
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import logging
import yaml
import json
import motor_controller  # Import the motor control module

# --- Load Configuration ---
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

SERVER_URI = config["server_uri"]

# --- Initialize FastAPI ---
app = FastAPI()

# --- Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Motor Queue ---
motor_queue = asyncio.Queue()

# --- WebSocket Client ---
class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.connection = None

    async def connect(self):
        while True:
            try:
                logger.info(f"Connecting to server at {self.uri}")
                self.connection = await websockets.connect(self.uri)
                logger.info("Connected to server")
                break
            except Exception as e:
                logger.error(f"Connection failed: {e}")
                await asyncio.sleep(5)

    async def send(self, message: str):
        if self.connection:
            await self.connection.send(message)

    async def receive(self):
        if self.connection:
            return await self.connection.recv()

ws_client = WebSocketClient(SERVER_URI)

# --- Server Listener ---
async def listen_server():
    await ws_client.connect()
    while True:
        try:
            message = await ws_client.receive()
            logger.info(f"Received from server: {message}")
            data = json.loads(message)

            # Dispatch based on data type
            if data.get("type") == "joystick":
                await motor_queue.put(data)
        except Exception as e:
            logger.error(f"Error in receive loop: {e}")
            await ws_client.connect()  # Reconnect

# --- Motor Control Task ---
async def run_motor():
    while True:
        data = await motor_queue.get()
        left_val = data.get("left_motor", 0)
        right_val = data.get("right_motor", 0)
        logger.info(f"Motor command: left={left_val}, right={right_val}")

        motor_controller.set_motor(left_val, right_val)
        motor_queue.task_done()

# --- FastAPI Endpoints ---
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    motor_controller.init_gpio()  # GPIO setup
    asyncio.create_task(listen_server())
    asyncio.create_task(run_motor())

@app.on_event("shutdown")
async def shutdown_event():
    motor_controller.cleanup_gpio()  # GPIO cleanup

# --- Run FastAPI ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("FastClient:app", host="0.0.0.0", port=5000, reload=False)




# import asyncio
# import websockets
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# import logging
# import yaml

# # Load configuration
# with open("config.yaml", "r") as f:
#     config = yaml.safe_load(f)

# SERVER_URI = config["server_uri"]

# # Initialize FastAPI app
# app = FastAPI()

# # Setup logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Shared WebSocket connection
# class WebSocketClient:
#     def __init__(self, uri):
#         self.uri = uri
#         self.connection = None

#     async def connect(self):
#         while True:
#             try:
#                 logger.info(f"Connecting to server at {self.uri}")
#                 self.connection = await websockets.connect(self.uri)
#                 logger.info("Connected to server")
#                 break
#             except Exception as e:
#                 logger.error(f"Connection failed: {e}")
#                 await asyncio.sleep(5)  # Retry delay

#     async def send(self, message: str):
#         if self.connection:
#             await self.connection.send(message)

#     async def receive(self):
#         if self.connection:
#             return await self.connection.recv()

# # Initialize client
# ws_client = WebSocketClient(SERVER_URI)

# # Background task to listen for server messages
# async def listen_server():
#     await ws_client.connect()
#     while True:
#         try:
#             message = await ws_client.receive()
#             logger.info(f"Received from server: {message}")
#             # Dispatch to services (to be implemented)
#         except Exception as e:
#             logger.error(f"Error in receive loop: {e}")
#             await ws_client.connect()  # Reconnect on failure

# # FastAPI route for health check
# @app.get("/health")
# async def health():
#     return {"status": "ok"}

# # FastAPI startup event to launch background task
# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(listen_server())

# # Local WebSocket endpoint for testing (optional)
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             logger.info(f"Local WS received: {data}")
#             await websocket.send_text(f"Echo: {data}")
#     except WebSocketDisconnect:
#         logger.info("Local WebSocket disconnected")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("FastClient:app", host="0.0.0.0", port=5000, reload=False)

