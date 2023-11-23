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

    # Change the active frame
    def changeFrame(self, frame):
        pass

    # Draw the landmarks on the active frame
    def drawLandmarks(self, landmarks):
        pass

    # Draw the counter on the active frame
    def drawCounter(self, count):
        pass

    # Show the frame
    def show(self):
        pass

    # Close the window
    def close(self):
        pass


class OpenCVPoseDetectorPreviewer(PoseDetectorPreviewer):

    def __init__(self):
        self.windowName = "MediaPipe Pose"

        self.count = None
        self.activeFrame = None

    # Opens the window
    def open(self):
        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)

    # Wait till a key is pressed
    def wait(self, quitButton='q') -> None:
        if cv2.waitKey(1) & 0xFF == ord(quitButton):
            exit(0)

    def changeFrame(self, frame):
        self.activeFrame = frame

    def drawLandmarks(self, landmarks):
        if landmarks is None:
            return
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in
            landmarks
        ])
        mp.solutions.drawing_utils.draw_landmarks(
            self.activeFrame,
            pose_landmarks_proto,
            mp.solutions.pose.POSE_CONNECTIONS,
            mp.solutions.drawing_styles.get_default_pose_landmarks_style()
        )

    def drawCounter(self, count):
        self.count = count

    def show(self):
        # The counter should be shown on every frame, so we draw it here and track it in the class
        if self.count is not None:
            # Big white text in top left corner
            cv2.putText(self.activeFrame, str(self.count), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4,
                        cv2.LINE_AA)

        if self.activeFrame is not None:
            cv2.imshow(self.windowName, self.activeFrame)
            self.activeFrame = None

    # Close the window
    def close(self):
        cv2.destroyAllWindows()
