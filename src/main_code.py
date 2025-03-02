import cv2
import time
import signal
from camera_opencv import CameraProcessor
from rover.drivetrain import Drivetrain
from rover.sonar import Sonar
from rover.sonar_led import SonarLEDS

# Initialize drivetrain and sonar
drivetrain = Drivetrain()
sonar = Sonar()

def signal_handler(sig, frame):
    drivetrain.set_motion(speed=0, heading=0, angular_speed=0)
    print("Stopping...")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

def spin_in_place():
    drivetrain.set_motion(speed=0, heading=0, angular_speed=50)  # Rotate in place

def stop_movement():
    drivetrain.set_motion(speed=0, heading=0, angular_speed=0)

def move_forward_until_distance(target_distance=2, speed=100):
    """Moves the robot forward until it's within `target_distance` inches of an object."""
    print("Moving towards the ball...")
    while True:
        distance = sonar.get_distance() / 25.4  # Convert mm to inches
        print(f"Current distance: {distance:.2f} inches")
        
        if distance <= target_distance:
            print("Reached target distance. Stopping.")
            break
        
        drivetrain.set_motion(speed=speed, heading=90, angular_speed=0)
        time.sleep(0.1)  # Short sleep to avoid excessive updates

    stop_movement()

def main():
    sonar_leds = SonarLEDS()
    sonar_leds.setRGBMode(0)
    time.sleep(1)

    sonar_leds.left.setPixelColor(0xFF0000)
    sonar_leds.right.setPixelColor(0xFF0000)
    camera = CameraProcessor()
    spin_in_place()  # Start spinning in place

    start_time = time.time()
    max_runtime = 20  # Timeout after 20 seconds if ball not detected

    while time.time() - start_time < max_runtime:
        frame = camera.get_frame()
        if frame is None:
            print("Failed to grab frame")
            break

        # Process frame for blue ball detection
        processed_frame, ball_detected = camera.detect_blue_ball(frame)

        # Show camera output
        cv2.imshow("Camera Output", processed_frame)

        # If ball detected, stop spinning and move forward
        if ball_detected:
            print("Blue ball detected! Stopping...")
            stop_movement()
            time.sleep(1)

            move_forward_until_distance(target_distance=10, speed=100)  # Move forward using sonar
            break

        # Exit loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exit key pressed. Stopping...")
            break

    if time.time() - start_time >= max_runtime:
        print("Max runtime reached. No ball detected. Stopping...")

    # Stop movement after the loop ends
    stop_movement()

    # Release resources
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
