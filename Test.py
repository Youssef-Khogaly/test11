import pigpio
from enum import Enum
import array
import time

# care pin 12,18 share pwm channel 0 and gpio 13,19 share pwm channel 1
# only 1 pin from each channel can be active at a time
class HardwarePWMPin(Enum):
    PWM0_GPIO12 = 12  # PWM channel 0
    PWM0_GPIO18 = 18  # PWM channel 0
    PWM1_GPIO13 = 13  # PWM channel 1
    PWM1_GPIO19 = 19  # PWM channel 1

class DcMotorPWM:
    def __init__(self, pwm_pin: HardwarePWMPin, max_rpm=95, frequency=1000, pwm_resolution=255):
        self.pwm_pin = pwm_pin
        self.max_rpm = max_rpm
        self.frequency = frequency
        self.pwm_resolution = pwm_resolution
        self.pi = pigpio.pi()

        if not self.pi.connected:
            raise IOError("Could not connect to pigpio daemon.")
        
        self.pi.set_mode(self.pwm_pin.value, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(self.pwm_pin.value, self.frequency)
        self.pi.set_PWM_range(self.pwm_pin.value, self.pwm_resolution)

        self._build_lookup_table()
        self.set_rpm(0)

    def _build_lookup_table(self):
        """Create a cached lookup from RPM to PWM value using an array (uint8_t)."""
        self.rpm_to_pwm = array.array('B', [0] * (self.max_rpm + 1))
        for rpm in range(self.max_rpm + 1):
            duty_cycle_percent = (rpm / self.max_rpm) * 100
            pwm_value = round(duty_cycle_percent * self.pwm_resolution / 100)
            self.rpm_to_pwm[rpm] = pwm_value

    def set_rpm(self, rpm):
        """Set motor speed using cached lookup."""
        rpm = max(0, min(rpm, self.max_rpm))
        pwm_value = self.rpm_to_pwm[rpm]
        self.pi.set_PWM_dutycycle(self.pwm_pin.value, pwm_value)

    def stop(self):
        self.pi.set_PWM_dutycycle(self.pwm_pin.value, 0)

    def cleanup(self):
        self.stop()
        self.pi.stop()

def main():
    try:
        motor = DcMotorPWM(HardwarePWMPin.PWM0_GPIO12, max_rpm=95, frequency=1000)
        print("Running motor at 70 RPM. Press Ctrl+C to stop.")
        while True:
            motor.set_rpm(80)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping motor and cleaning up.")
        motor.cleanup()

if __name__ == "__main__":
    main()
