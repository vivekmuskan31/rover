# communication_manager.py

import asyncio
import json
import websockets
from typing import List

from utils import get_logger

class CommunicationManager:
    _instance = None

    def __init__(self, server_uri: str):
        self.server_uri = server_uri
        self.connection = None
        self.sensors = []
        self.controllers = []
        self._lock = asyncio.Lock()
        self.controller_routing_table = {
          "motor_cmd" : "MotorController",
        }
        self.logger = get_logger("ComManager")

    @classmethod
    def get_instance(cls, server_uri: str = None):
        if cls._instance is None:
            if server_uri is None:
                raise ValueError("server_uri must be provided on first initialization")
            cls._instance = cls(server_uri)
        return cls._instance

    def register_sensor(self, sensor):
        self.sensors.append(sensor)

    def register_controller(self, controller):
        self.controllers.append(controller)

    async def connect_to_server(self):
        while True:
            try:
                self.logger.info(f"Connecting to {self.server_uri}")
                self.connection = await websockets.connect(self.server_uri)
                self.logger.info(f"[Connection Succeeded] : {self.server_uri}")
                break
            except Exception as e:
                self.logger.warn(f"[Connection Failed]: {e}")
                await asyncio.sleep(5)

    async def send(self, data: dict):
        if self.connection is None:
            return False
        async with self._lock:
            try:
                await self.connection.send(json.dumps(data))
                return True
            except Exception as e:
                self.logger.error(f"[Send Failed]: {e}")
                return False

    async def receive_loop(self):
        while True:
            try:
                message = await self.connection.recv()
                data = json.loads(message)
                self.logger.info(f'[Received] : {data}')
                await self.route_incoming(data)
            except Exception as e:
                self.logger.info(f"[Receive Failed] : {e}")
                await self.connect_to_server()

    async def route_incoming(self, data: dict):
            type = data["type"]
            # controller = self.controller_routing_table.get(type, "DEFAULT") # Default will simply print the data
            controller = self.controllers[0]
            # self.logger.info(f"[Routing] : data['{type}'] -> {controller}")
            await controller.handle_command(data)

    async def start_all(self):
        await self.connect_to_server()
        asyncio.create_task(self.receive_loop())
        for sensor in self.sensors:
            asyncio.create_task(sensor.start())
    
    def clean_all(self):
        for controller in self.controllers:
            controller.cleanup()