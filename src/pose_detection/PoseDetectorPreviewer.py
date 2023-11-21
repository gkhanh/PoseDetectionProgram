import cv2


class PoseDetectorPreviewer:

    # Opens the window
    def open(self):
        pass

    # Wait till a key is pressed
    def wait(self):
        pass

    # Draw a frame on the window
    def draw(self, frame):
        pass

    # Close the window
    def close(self):
        pass


class OpenCVPoseDetectorPreviewer(PoseDetectorPreviewer):

    def __init__(self):
        self.windowName = "MediaPipe Pose"

    # Opens the window
    def open(self):
        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)

    # Wait till a key is pressed
    def wait(self, quitButton='q') -> None:
        if cv2.waitKey(1) & 0xFF == ord(quitButton):
            exit(0)

    # Draw a frame on the window
    def draw(self, frame):
        cv2.imshow(self.windowName, frame)

    # Close the window
    def close(self):
        cv2.destroyAllWindows()
