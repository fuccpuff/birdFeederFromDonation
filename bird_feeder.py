# sudo apt-get install python3-gpiozero

from gpiozero import Servo
from time import sleep

SERVO_PIN = 18
servo = Servo(SERVO_PIN)

def dispense_feed():
    servo.min()
    sleep(0.5)
    servo.max()
    sleep(0.5)
    servo.detach()  # Detach servo to save power and reduce jitter.

if __name__ == "__main__":
    dispense_feed()


# Remember to replace YOUR_RASPBERRY_PI_IP, YOUR_RASPBERRY_PI_USERNAME, YOUR_RASPBERRY_PI_PASSWORD, and /path/to/bird_feeder.py with the appropriate values.

# a. Connect a servo motor to your Raspberry Pi. Typically, the servo has three wires: power (red), ground (black/brown), and signal (white/yellow). Connect the power and ground wires to the 5V and GND pins on the Raspberry Pi, respectively. Connect the signal wire to a GPIO pin (e.g., GPIO18).
# b. Assemble the bird feeder with a mechanism that dispenses a small portion of bird feed when the servo motor rotates. You can use a simple gate mechanism that opens and closes to control the amount of bird feed dispensed.