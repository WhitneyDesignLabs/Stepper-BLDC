DEBOUNCE_TIME = 200  # Define it here if this value is not going to change, or if it is exclusive to this file.

import utime
import machine

class Channel:
    """
    The Channel class is used to define a logical control channel,
    typically representing an axis of motion. Each channel monitors
    input pins for step and direction signals and passes them to
    the associated motors.
    """
    def __init__(self, name, step_pin, dir_pin):
        self.name = name
        self.step_pin = machine.Pin(step_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.dir_pin = machine.Pin(dir_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.mapped_motors = []  # Stores the motors that are controlled by this channel
        self.last_step_time = utime.ticks_us()
        self.last_interrupt_time = utime.ticks_us()
        self.debounce_time = DEBOUNCE_TIME
        # Setup an interrupt to detect rising edge on the step pin
        self.step_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=self.step_counter_isr)

    def add_motor(self, motor, direction_multiplier=1):
        """
        Maps a motor to this channel with an optional direction multiplier
        to reverse the direction of motion.
        """
        self.mapped_motors.append((motor, direction_multiplier))

    def process(self):
        """
        Process the channel's state and pass the relevant information
        to each mapped motor for them to act upon.
        """
        current_time = utime.ticks_us()
        for motor, direction_multiplier in self.mapped_motors:
            motor.loop(current_time, self.last_step_time, self.dir_pin, direction_multiplier)

    def step_counter_isr(self, pin):
        """
        The Interrupt Service Routine called on a rising edge of the step pin.
        It updates the last step time and last interrupt time.
        """
        current_interrupt_time = utime.ticks_us()
        if utime.ticks_diff(current_interrupt_time, self.last_interrupt_time) <= self.debounce_time:
            return  # Ignore if the interrupt is within the debounce time
        self.last_step_time = current_interrupt_time
        self.last_interrupt_time = current_interrupt_time
        # Set motor_running to True for all mapped motors as a step has been detected
        for motor, _ in self.mapped_motors:
            motor.motor_running = True