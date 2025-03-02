import cv2
import numpy as np

class CameraProcessor:
    def __init__(self):
        """Initializes the camera for capturing video."""
        self.cap = cv2.VideoCapture(0)  # Use the default camera
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            exit()

    def get_frame(self):
        """Captures a frame from the camera."""
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def detect_blue_ball(self, frame):
        """Detects a blue ball in the provided frame."""
        # Convert the frame from BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the range of colors
        lower_blue = np.array([100, 150, 50])  # Lower bound of blue
        upper_blue = np.array([140, 255, 255])  # Upper bound of blue
        
        upper_red = np.array([255, 171, 171])  # Lower bound of red
        lower_red = np.array([163, 33, 33])  # Upper bound of red
        

        upper_green = np.array([168, 201, 119])  # Lower bound of green
        lower_green = np.array([117, 191, 6])  # Upper bound of green

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Bitwise-AND the mask and the original image
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        ball_detected = False
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # Minimum contour area to detect a ball
                ball_detected = True
                # Get the bounding box of the contour
                x, y, w, h = cv2.boundingRect(contour)
                # Draw the rectangle around the detected ball
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return frame, ball_detected

    def release(self):
        """Releases the camera resource."""
        self.cap.release()
