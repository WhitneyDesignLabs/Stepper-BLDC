MAX_PWM_VALUE = 65535  # The maximum duty cycle for the PWM signal, 16-bit value
PWM_FREQ = 1000  # The frequency of the PWM signal to control the motor speed
STEP_TIMEOUT = 50000  # Microseconds to stop the motor if no step pulse has been received

import machine
import utime

class BLDCMotor:
    """
    The BLDCMotor class represents a Brushless DC motor.
    It uses a PWM signal to control the speed of the motor
    based on the frequency of the step signal received from the Channel.
    """
    def __init__(self, name, motor_pwm_pin, dir_out_pin, brake_pin, brake_mode):
        self.name = name
        self.dir_out_pin = machine.Pin(dir_out_pin, machine.Pin.OUT)
        self.brake_pin = machine.Pin(brake_pin, machine.Pin.OUT)
        self.motor_pwm_pin = motor_pwm_pin
        self.pwm = machine.PWM(machine.Pin(motor_pwm_pin))
        self.frequency_to_pwm_ratio = MAX_PWM_VALUE / PWM_FREQ
        self.step_timeout = STEP_TIMEOUT
        if brake_mode not in ["autobrake", "coast"]:
            raise ValueError("Invalid brake_mode! Choose between 'autobrake' and 'coast'")
        self.brake_mode = brake_mode
        self.motor_running = False
        self.setup_pwm()

    def setup_pwm(self):
        """
        Setup PWM frequency and initial duty cycle.
        """
        self.pwm.freq(PWM_FREQ)
        self.pwm.duty_u16(0)

    def loop(self, current_time, last_step_time, dir_pin, direction_multiplier):
        """
        Calculate elapsed time since the last step, set the motor speed,
        and update the direction of the motor based on the received direction signal.
        """
        elapsed_time = utime.ticks_diff(current_time, last_step_time)
        if self.motor_running:
            if elapsed_time > self.step_timeout:
                self.stop_motor()  # Stop the motor if no steps received in the allowed time
            if elapsed_time > 0:
                frequency = 1e6 / elapsed_time  # Calculate the frequency of the step signal
                self.set_motor_speed(frequency)
        direction = dir_pin.value()
        if direction_multiplier == -1:
            direction = 1 - direction  # Reverse the direction if the multiplier is -1
        self.dir_out_pin.value(direction)

    def set_motor_speed(self, frequency):
        """
        Set the motor speed using PWM duty cycle based on the received step signal frequency.
        """
        if self.motor_running:
            pwm_value = min(int(frequency * self.frequency_to_pwm_ratio), MAX_PWM_VALUE)
            self.pwm.duty_u16(pwm_value)
            self.brake_pin.value(0)  # Release the brake when the motor is running

    def stop_motor(self):
        """
        Stop the motor and apply the brake if brake_mode is set to 'autobrake'.
        """
        self.pwm.duty_u16(0)
        self.motor_running = False
        print(f"{self.name} Motor Stopped")
        if self.brake_mode == "autobrake":
            self.brake_pin.value(1)
        else:
            self.brake_pin.value(0)