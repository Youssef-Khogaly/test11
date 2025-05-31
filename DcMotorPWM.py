import pigpio
from enum import Enum
import array

# care pin 12,18 share pwm channel 0 and gpio 13,19 share pwm channel 1
# only 1 pin from each channel can be active at a time
class HardwarePWMPin(Enum):
    PWM0_GPIO12 = 12  # PWM channel 0
    PWM0_GPIO18 = 18  # PWM channel 0
    PWM1_GPIO13 = 13  # PWM channel 1
    PWM1_GPIO19 = 19  # PWM channel 1

# make sure pigpio daemon running
# sudo  pigpio

# to start it automatically
# sudo systemctl enable pigpiod
# sudo systemctl start pigpiod

# A wrapper class for dc motor mosfet driver control
# 1 direction
class DcMotorPWM:
    def __init__(self, pwm_pin: HardwarePWMPin, max_rpm=95, frequency=1000):
        self.pwm_pin = pwm_pin
        self.max_rpm = max_rpm
        self.frequency = frequency
        self.pi = pigpio.pi()

        # make sure pigpio daemon running
        if not self.pi.connected:
            raise IOError("Could not connect to pigpio daemon.")
        
        self.pi.set_mode(self.pwm_pin.value, pigpio.OUTPUT)  # Use the value of the enum
        self.pi.set_PWM_frequency(self.pwm_pin.value, self.frequency)
        
        self._build_lookup_table()
        self.set_rpm(0)

    # build a lookup table for rpm to duty cycle instead of repeat heavy floating point calculation every time
    def _build_lookup_table(self):
        """Create a cached lookup from RPM to PWM value using an array (uint8_t)."""
        # Use the 'B' typecode for an unsigned 8-bit integer array
        self.rpm_to_pwm = array.array('B', [0] * (self.max_rpm + 1))  # array of uint8_t
        for rpm in range(self.max_rpm + 1):
            duty_cycle_percent = (rpm / self.max_rpm) * 100  # rpm to duty cycle percent
            pwm_value = round(duty_cycle_percent * 255 / 100)  # duty cycle percent to pwm value
            self.rpm_to_pwm[rpm] = pwm_value

    def set_rpm(self, rpm):
        """Set motor speed using cached lookup."""
        rpm = max(0, min(rpm, self.max_rpm))  # make sure rpm in the valid range 0~max rpm
        pwm_value = self.rpm_to_pwm[rpm]  # get the pwm value from the lookup table
        self.pi.set_PWM_dutycycle(self.pwm_pin.value, pwm_value)  # Use the value of the enum for the pin

    def stop(self):
        self.pi.set_PWM_dutycycle(self.pwm_pin.value, 0)

    def cleanup(self):
        self.stop()
        self.pi.stop()
