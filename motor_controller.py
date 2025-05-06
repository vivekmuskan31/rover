import RPi.GPIO as GPIO

# --- GPIO Pin Mapping (BCM Mode) ---
IN1_LEFT = 17
IN2_LEFT = 27
ENA_LEFT = 18  # PWM

IN3_RIGHT = 23
IN4_RIGHT = 22
ENB_RIGHT = 24  # PWM

FREQ = 100  # PWM frequency in Hz

# --- Setup ---
def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1_LEFT, GPIO.OUT)
    GPIO.setup(IN2_LEFT, GPIO.OUT)
    GPIO.setup(ENA_LEFT, GPIO.OUT)
    GPIO.setup(IN3_RIGHT, GPIO.OUT)
    GPIO.setup(IN4_RIGHT, GPIO.OUT)
    GPIO.setup(ENB_RIGHT, GPIO.OUT)

    global pwm_left, pwm_right
    pwm_left = GPIO.PWM(ENA_LEFT, FREQ)
    pwm_right = GPIO.PWM(ENB_RIGHT, FREQ)
    pwm_left.start(0)  # Motors off initially
    pwm_right.start(0)

# --- Set Motor Values ---
def set_motor(left_val: float, right_val: float):
    """
    left_val, right_val: Range [-1.0, 1.0]
    Controls direction + speed.
    """

    # --- LEFT Motor Group (1 & 4) ---
    if left_val >= 0:
        GPIO.output(IN1_LEFT, GPIO.HIGH)
        GPIO.output(IN2_LEFT, GPIO.LOW)
    else:
        GPIO.output(IN1_LEFT, GPIO.LOW)
        GPIO.output(IN2_LEFT, GPIO.HIGH)

    duty_left = abs(left_val) * 100  # Map [-1,1] to [0,100]
    pwm_left.ChangeDutyCycle(duty_left)

    # --- RIGHT Motor Group (2 & 3) ---
    if right_val >= 0:
        GPIO.output(IN3_RIGHT, GPIO.HIGH)
        GPIO.output(IN4_RIGHT, GPIO.LOW)
    else:
        GPIO.output(IN3_RIGHT, GPIO.LOW)
        GPIO.output(IN4_RIGHT, GPIO.HIGH)

    duty_right = abs(right_val) * 100
    pwm_right.ChangeDutyCycle(duty_right)

# --- Cleanup ---
def cleanup_gpio():
    global pwm_left, pwm_right
    try:
        pwm_left.stop()
        pwm_right.stop()
    except Exception as e:
        print(f"PWM stop error: {e}")
    GPIO.cleanup()
