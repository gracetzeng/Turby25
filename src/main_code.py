import cv2
import time
import signal
from camera_opencv import CameraProcessor
from rover.drivetrain import Drivetrain
from rover.sonar import Sonar

# Initialize drivetrain and sonar
drivetrain = Drivetrain()
sonar = Sonar()  # Initialize the Sonar object

def signal_handler(sig, frame):
    drivetrain.set_motion(speed=0, heading=0, angular_speed=0)
    print("Stopping...")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

def spin_in_place():
    drivetrain.set_motion(speed=0, heading=0, angular_speed=50)

def stop_movement():
    drivetrain.set_motion(speed=0, heading=0, angular_speed=0)

def move_toward_ball():
    while True:
        # Get the distance from the sonar sensor
        distance = sonar.get_distance()  # Returns distance in inches
        print(f"Current distance: {distance} inches")

        # If the robot is within 2 inches of the ball, stop
        if distance <= 2:
            print("Ball is close enough. Stopping...")
            stop_movement()
            break
        else:
            # Move towards the ball
            drivetrain.set_motion(speed=50, heading=0, angular_speed=0)

        # Give some time before checking the distance again
        time.sleep(0.5)

def main():
    camera = CameraProcessor()
    spin_in_place()  # Start spinning in place

    start_time = time.time()
    max_runtime = 30  # Set timeout after 30 seconds if ball not detected

    while time.time() - start_time < max_runtime:
        frame = camera.get_frame()
        if frame is None:
            print("Failed to grab frame")
            break

        # Process frame for blue ball detection
        processed_frame, ball_detected = camera.detect_blue_ball(frame)

        # Camera output
        cv2.imshow("Camera Output", processed_frame)

        # If ball detected, stop moving and move towards the ball
        if ball_detected:
            print("Blue ball detected! Stopping spin and moving towards ball...")
            stop_movement()
            move_toward_ball()  # Move towards the ball based on sonar sensor
            break

        # Exit loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exit key pressed. Stopping.")
            break

    if time.time() - start_time >= max_runtime:
        print("Max runtime reached, no ball detected. Stopping.")
    
    # Stop movement after the loop ends
    stop_movement()

    # Release resources
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
