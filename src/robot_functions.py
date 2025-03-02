from rover.motor import Motor
from rover.drivetrain import Drivetrain

class Drivetrain:
    def __init__(self):
        self.front_left_motor = Motor()
        self.front_right_motor = Motor()
        self.rear_left_motor = Motor()
        self.rear_right_motor = Motor()

    def set_motion(self, speed=0, heading=0, angular_speed=0):
        """Set the robot's motion speed, heading, and angular speed."""
        # Speed controls forward/backward motion
        # Heading controls direction (0 = right, 90 = forward, 180 = left, etc.)
        # Angular speed controls rotation (positive for counterclockwise, negative for clockwise)
        self.front_left_motor.set_speed(speed)
        self.front_right_motor.set_speed(speed)
        self.rear_left_motor.set_speed(speed)
        self.rear_right_motor.set_speed(speed)

    def stop(self):
        """Stop all robot motion."""
        self.front_left_motor.stop()
        self.front_right_motor.stop()
        self.rear_left_motor.stop()
        self.rear_right_motor.stop()
