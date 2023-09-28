# Stepper-BLDC
A project to convert stepper motor step &amp; direction signals and convert to pwm for brushless DC motor use
Description:
This project provides a scalable and modular Python-based solution to control Brushless DC Motors (BLDC) using input signals (step and direction) typically used for stepper motors, essentially allowing users to replace stepper motors with more efficient BLDC motors without changing the control hardware/software. It’s designed to run on microcontrollers compatible with MicroPython, like the ESP32, offering a lightweight and efficient solution for various automation tasks.

Use Case:
Ideal for applications such as CNC machines, 3D printers, robotics, or any domain where precise motor control is essential, and upgrading to BLDC motors can offer benefits in terms of efficiency, speed, and torque. For instance, in a CNC machine, users can replace the existing stepper motors with BLDC motors to achieve higher speeds, better energy efficiency, and reduced heat generation, thereby enhancing the overall performance and longevity of the machine.

Example Configurations:
Example 1: Single Channel Configuration
In this configuration, one channel is controlling two motors. The motors are mapped to the 'x' channel, with motor 'A' having a direction multiplier of -1, and motor 'B' having a direction multiplier of 1.

python
Copy code
from lib.channel import Channel
from lib.bldcmotor import BLDCMotor

# Define a single channel
channel_x = Channel('x', step_pin=2, dir_pin=4)

# Define two motors and set brake mode to "autobrake" or "coast"
motor_a = BLDCMotor('A', motor_pwm_pin=12, dir_out_pin=14, brake_pin=16, brake_mode="autobrake")

motor_b = BLDCMotor('B', motor_pwm_pin=13, dir_out_pin=15, brake_pin=17, brake_mode="coast")


# Map motors to the 'x' channel
channel_x.add_motor(motor_a, direction_multiplier=-1)

channel_x.add_motor(motor_b, direction_multiplier=1)


channels = [channel_x]

Example 2: Dual Channel Configuration
In this example, two channels are defined, each controlling two motors. This can be representative of a scenario like a 3D printer where each axis can be controlled by a different channel.

python
Copy code
from lib.channel import Channel
from lib.bldcmotor import BLDCMotor

# Define two channels
channel_x = Channel('x', step_pin=2, dir_pin=4)

channel_y = Channel('y', step_pin=3, dir_pin=5)


# Define four motors
motor_a = BLDCMotor('A', motor_pwm_pin=12, dir_out_pin=14, brake_pin=16, brake_mode="autobrake")

motor_b = BLDCMotor('B', motor_pwm_pin=13, dir_out_pin=15, brake_pin=17, brake_mode="autobrake")

motor_c = BLDCMotor('C', motor_pwm_pin=18, dir_out_pin=20, brake_pin=22, brake_mode="autobrake")

motor_d = BLDCMotor('D', motor_pwm_pin=19, dir_out_pin=21, brake_pin=23, brake_mode="autobrake")


# Map motors to channels
channel_x.add_motor(motor_a, direction_multiplier=-1)

channel_x.add_motor(motor_b, direction_multiplier=1)

channel_y.add_motor(motor_c, direction_multiplier=-1)

channel_y.add_motor(motor_d, direction_multiplier=1)


channels = [channel_x, channel_y]

In each configuration, after defining the channels and mapping the motors, the program will listen to the step/dir signals and control the respective motors accordingly.
