import pigpio
from enum import Enum
import array

# Enum for hardware PWM pins (same as before)
class HardwarePWMPin(Enum):
    PWM0_GPIO12 = 12  # PWM channel 0
    PWM0_GPIO18 = 18  # PWM channel 0
    PWM1_GPIO13 = 13  # PWM channel 1
    PWM1_GPIO19 = 19  # PWM channel 1

# A wrapper class for Servo motor control
class ServoMotorPWM:
    def __init__(self, pwm_pin: HardwarePWMPin,max_angle=180,frequency=50 ):
        self.pwm_pin = pwm_pin
        self.frequency = frequency
        self.max_angle = max_angle
        self.pi = pigpio.pi()

        # Make sure pigpio daemon is running
        if not self.pi.connected:
            raise IOError("Could not connect to pigpio daemon.")
        
        self.pi.set_mode(self.pwm_pin.value, pigpio.OUTPUT)  # Use the value of the enum
        self.pi.set_PWM_frequency(self.pwm_pin.value, self.frequency)  # Servo frequency (50Hz)
        
        # Build the lookup table for angle to pulse width
        self._build_lookup_table()
        
    def _build_lookup_table(self):
        """Create a cached lookup from angle to pulse width."""
        # Use the 'H' typecode for an unsigned short (16-bit) array
        self.angle_to_pulsewidth = array.array('H', [0] * (self.max_angle + 1))  # Array to store pulse widths
        
        # Precompute pulse widths for each angle (0 to max_angle)
        for angle in range(self.max_angle + 1):
            pulse_width = (angle / self.max_angle) * 1000 + 1000  # Map angle (0-180) to pulse width (1000-2000 µs)
            self.angle_to_pulsewidth[angle] = round(pulse_width)
    
    def set_angle(self, angle):
        """Set the servo position based on the cached pulse width from the lookup table."""
        # Ensure the angle is within the valid range 
        angle = max(0, min(self.max_angle, angle))
        
        # Get the pulse width from the lookup table for the given angle
        pulse_width = self.angle_to_pulsewidth[angle]
        
        # Set the servo pulse width (in microseconds)
        self.pi.set_servo_pulsewidth(self.pwm_pin.value, pulse_width)

    def stop(self):
        """Stop the servo motor by turning off the PWM."""
        self.pi.set_servo_pulsewidth(self.pwm_pin.value, 0)

    def cleanup(self):
        """Clean up and stop the servo motor."""
        self.stop()
        self.pi.stop()
