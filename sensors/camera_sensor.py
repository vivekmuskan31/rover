# camera_sensor.py (picamera2 version)

import asyncio
import time
import base64
from picamera2 import Picamera2, Preview

from utils import get_logger
from sensors.sensor import BaseSensor
from communication_manager import CommunicationManager

import io
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

class CameraSensor(BaseSensor):
    def __init__(self, name="CameraSensor"):
        super().__init__(name)
        self.picam = Picamera2()
        self.seq = 0
        self.FPS = 10
        self.logger = get_logger(self.name)
        self.executor = ThreadPoolExecutor(max_workers=1)

        # Configure resolution
        self.picam.configure(
            self.picam.create_still_configuration(
                main={"size": (640, 480)}  # Lower resolution for performance
            )
        )

    async def start(self):
        self.picam.start()
        await asyncio.sleep(1)  # short warm-up

        while True:
            frame = self.picam.capture_array()
            loop = asyncio.get_running_loop()
            encoded_image, size_kb = await loop.run_in_executor(
                self.executor, self.encode_image, frame
            )

            payload = {
                "type": "camera_frame",
                "timestamp": time.time(),
                "seq": self.seq,
                "data": encoded_image,
            }
            payload_log = {
                "seq": self.seq,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(payload["timestamp"])),
                "data" : f"<{size_kb:.2f} KB>"
            }
            self.seq += 1

            comm = CommunicationManager.get_instance()
            await comm.send(payload)
            self.logger.info(f"[SENT] : {payload_log}")
            # await asyncio.sleep(1 / self.FPS)

    def encode_image(self, frame):
        image = Image.fromarray(frame)
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        size_kb = len(buffer.getvalue()) / 1024
        encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return encoded_image, size_kb

    def get_data(self):
        self.picam.start()
        frame = self.picam.capture_array()
        return frame

    def test(self):
        frame = self.get_data()
        if frame is not None:
            self.logger.info(f"[{self.name}] Frame captured (shape={frame.shape})")
        else:
            self.logger.info(f"[{self.name}] No frame captured")
