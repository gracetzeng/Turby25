import cv2
import numpy as np

class CameraProcessor:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Unable to access camera.")
            exit(1)

    def get_frame(self):
        """Captures a single frame from the camera."""
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            return None
        return frame
    
    def detect_blue_ball(self, frame):
        # Convert the image from BGR to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define lower and upper bound on blue color
        lower_blue = np.array([100, 150, 150])
        upper_blue = np.array([140, 255, 255])

        # Create a mask to isolate the blue areas
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        ball_detected = False
        if contours:
            # Find the largest contour (hopefully the ball)
            largest_contour = max(contours, key=cv2.contourArea)

            # Get the bounding box of the largest contour
            x, y, w, h = cv2.boundingRect(largest_contour)

            # If the size of the detected contour is significant, consider it a ball
            if w * h > 100:  # Threshold area to avoid false positives
                ball_detected = True
                # Draw a bounding box around the detected ball
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Return the processed frame and ball detection status
        return frame, ball_detected

    def release(self):
        self.cap.release()
