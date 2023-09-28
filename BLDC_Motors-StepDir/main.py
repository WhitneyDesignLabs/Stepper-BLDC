from lib.channel import Channel
from lib.bldcmotor import BLDCMotor

import utime

# Constants were move into corresponding classes

# Setup Channels and Motors and map them together.
channel_x = Channel('x', step_pin=2, dir_pin=4)

motor_a = BLDCMotor('A', motor_pwm_pin=12, dir_out_pin=14, brake_pin=16, brake_mode="autobrake")
motor_b = BLDCMotor('B', motor_pwm_pin=13, dir_out_pin=15, brake_pin=17, brake_mode="autobrake")

channel_x.add_motor(motor_a, direction_multiplier=-1)
channel_x.add_motor(motor_b, direction_multiplier=1)

channels = [channel_x]

print("Program is up and running, awaiting step/dir signals from the controller.")

# Main loop: Continuously process each channel.
while True:
    for channel in channels:
        channel.process()
        utime.sleep_us(10)
