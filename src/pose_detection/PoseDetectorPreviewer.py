import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2


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

    # Draw the landmarks on the frame
    def drawLandmarks(self, frame, landmarks):
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

    def drawLandmarks(self, frame, landmarks):
        if landmarks is None:
            return
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in
            landmarks
        ])
        mp.solutions.drawing_utils.draw_landmarks(
            frame,
            pose_landmarks_proto,
            mp.solutions.pose.POSE_CONNECTIONS,
            mp.solutions.drawing_styles.get_default_pose_landmarks_style()
        )

    # Close the window
    def close(self):
        cv2.destroyAllWindows()
