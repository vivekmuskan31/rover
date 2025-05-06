import RPi.GPIO as GPIO
import time

# --- BCM Pin Mapping ---
# pins = [17, 27, 18, 23, 22, 24]  # IN1, IN2, ENA, IN3, IN4, ENB
pins = [17, 18, 23, 24]  # IN1, IN2, ENA, IN3, IN4, ENB
# pins = range(29)

GPIO.setmode(GPIO.BCM)

# Set all pins as OUTPUT
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # Set HIGH

print("All pins set HIGH. Motors should spin.")

time.sleep(30)  # Run motors for 5 seconds

# Cleanup
GPIO.cleanup()
print("GPIO cleaned up.")
