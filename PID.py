

"""
a wrapper class for pid controll
"""

class PID:
    def __init__(self, kp, ki, kd):
        """
        Initialize the PID controller with given gains.
        
        :param kp: Proportional gain
        :param ki: Integral gain
        :param kd: Derivative gain
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.prev_error = 0.0  # Previous error value
        self.integral = 0.0    # Integral sum of error
    def compute(self, setpoint, actual_value, dt):
        """
        Compute the PID control output.

        :param setpoint: The desired target value.
        :param actual_value: The current actual value from the system.
        :param dt: Time interval since the last update.
        :return: The PID control output.
        """
        if dt <= 0:
            return 0  # Prevent division by zero or negative dt

        # Calculate error
        error = setpoint - actual_value

        # Proportional term
        proportional = self.kp * error

        # Integral term
        self.integral += error * dt
        integral_term = self.ki * self.integral

        # Derivative term
        derivative = self.kd * (error - self.prev_error) / dt

        # Update previous error
        self.prev_error = error

        # Compute total output
        output = proportional + integral_term + derivative
        return output

    def reset(self):
        """
        Reset the PID controller (clear integral and previous error).
        """
        self.prev_error = 0.0
        self.integral = 0.0

    def set_gains(self, kp, ki, kd):
        """
        Set new PID gains.

        :param kp: New Proportional gain
        :param ki: New Integral gain
        :param kd: New Derivative gain
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def get_gains(self):
        """
        Get the current PID gains.

        :return: A tuple (kp, ki, kd)
        """
        return self.kp, self.ki, self.kd