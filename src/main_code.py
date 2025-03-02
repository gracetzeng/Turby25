import cv2
import time
import signal
from camera_opencv import CameraProcessor
from rover.drivetrain import Drivetrain

# Initialize drivetrain
drivetrain = Drivetrain()

def signal_handler(sig, frame):
    drivetrain.set_motion(speed=0, heading=0, angular_speed=0)
    print("Stopping...")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

def spin_in_place():
    # Adjust angular_speed to control the rotation speed.
    drivetrain.set_motion(speed=0, heading=0, angular_speed=50)

def stop_movement():
    drivetrain.set_motion(speed=0, heading=0, angular_speed=0)

def main():
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

        # If ball detected, stop moving and exit
        if ball_detected:
            print("Blue ball detected! Stopping...")
            stop_movement()
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
