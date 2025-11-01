# motor_controller.py

import RPi.GPIO as GPIO
import time
import asyncio
from controllers.controller import BaseController
from utils import get_logger


IN1_LEFT = 17
IN2_LEFT = 27
ENA_LEFT = 18  # PWM
IN3_RIGHT = 23
IN4_RIGHT = 22
ENB_RIGHT = 24  # PWM
FREQ = 100  # Hz

class MotorController(BaseController):
    def __init__(self, name="MotorController"):
        super().__init__(name)
        self.pwm_left = None
        self.pwm_right = None
        self._init_gpio()
        self.logger = get_logger(self.name)

        self._last_cmd = (0.0, 0.0)
        self._last_cmd_time = time.time()
        self._loop_task = asyncio.create_task(self._motor_loop())


    def _init_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(IN1_LEFT, GPIO.OUT)
        GPIO.setup(IN2_LEFT, GPIO.OUT)
        GPIO.setup(ENA_LEFT, GPIO.OUT)
        GPIO.setup(IN3_RIGHT, GPIO.OUT)
        GPIO.setup(IN4_RIGHT, GPIO.OUT)
        GPIO.setup(ENB_RIGHT, GPIO.OUT)

        self.pwm_left = GPIO.PWM(ENA_LEFT, FREQ)
        self.pwm_right = GPIO.PWM(ENB_RIGHT, FREQ)
        self.pwm_left.start(0)
        self.pwm_right.start(0)

    def _set_motor_values(self, left_val: float, right_val: float):
        # Run Left motors 1&4
        if left_val >= 0:
            GPIO.output(IN1_LEFT, GPIO.HIGH)
            GPIO.output(IN2_LEFT, GPIO.LOW)
        else:
            GPIO.output(IN1_LEFT, GPIO.LOW)
            GPIO.output(IN2_LEFT, GPIO.HIGH)

        duty_left = abs(left_val) * 100 # Map [-1,1] to [0,100]
        self.pwm_left.ChangeDutyCycle(duty_left)

        # Run Right Motors 2&3
        if right_val >= 0:
            GPIO.output(IN3_RIGHT, GPIO.HIGH)
            GPIO.output(IN4_RIGHT, GPIO.LOW)
        else:
            GPIO.output(IN3_RIGHT, GPIO.LOW)
            GPIO.output(IN4_RIGHT, GPIO.HIGH)

        duty_right = abs(right_val) * 100
        self.pwm_right.ChangeDutyCycle(duty_right)
    
    async def _motor_loop(self):
        while True:
            now = time.time()
            if now - self._last_cmd_time > 0.2:  # idle timeout 200ms
                self._set_motor_values(0.0, 0.0)
            else:
                self._set_motor_values(*self._last_cmd)
            await asyncio.sleep(0.1)


    async def handle_command(self, data: dict):
        if data.get("type") != "motor_cmd":
            return
        left = float(data.get("left_motor", 0.0))
        right = float(data.get("right_motor", 0.0))
        self._last_cmd = (left, right)
        self._last_cmd_time = time.time()
    

    def cleanup(self):
        try:
            self.pwm_left.stop()
            self.pwm_right.stop()
        except Exception as e:
            self.logger.info(f"PWM stop error: {e}")
        GPIO.cleanup()

    def test(self, data: dict=None):
        if not data:
          data = {
            'type' : 'motor_cmd',
            'left_motor' : 0.5,
            'right_motor' : 0.5,
          }
        self.logger.info(f"[{self.name}] Testing with: {data}")
        self._set_motor_values(data.get("left_motor", 0.0), data.get("right_motor", 0.0))
