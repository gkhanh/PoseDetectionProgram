<<<<<<< HEAD
import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
=======
import textwrap
import cv2
from src.models.Measurement import LandmarkPosition
>>>>>>> master


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
<<<<<<< HEAD
    def drawLandmarks(self, landmarks):
=======
    def drawLandmarks(self, landmark):
        pass

    # Draw the processed landmarks on the active frame
    def drawFrameMeasurement(self, frameMeasurement):
>>>>>>> master
        pass

    # Draw the counter on the active frame
    def drawCounter(self, count):
        pass

<<<<<<< HEAD
=======
    # Display the result text
    def displayResult(self, stateText):
        pass

>>>>>>> master
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
        self.stateText = None
<<<<<<< HEAD
=======
        self.feedbackMessage = None
>>>>>>> master

    # Opens the window
    def open(self):
        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)

    # Wait till a key is pressed
    def wait(self, quitButton='q') -> None:
        if cv2.waitKey(1) & 0xFF == ord(quitButton):
            exit(0)

    def changeFrame(self, frame):
        self.activeFrame = frame

<<<<<<< HEAD
=======
    # Function to manually draw skeleton on the frame
    def drawFrameMeasurement(self, frameMeasurement):
        if not frameMeasurement:
            return

        landmarksToDraw = {
            LandmarkPosition.LEFT_SHOULDER, LandmarkPosition.RIGHT_SHOULDER,
            LandmarkPosition.LEFT_HIP, LandmarkPosition.RIGHT_HIP,
            LandmarkPosition.LEFT_ELBOW, LandmarkPosition.RIGHT_ELBOW,
            LandmarkPosition.LEFT_WRIST, LandmarkPosition.RIGHT_WRIST,
            LandmarkPosition.LEFT_KNEE, LandmarkPosition.RIGHT_KNEE,
            LandmarkPosition.LEFT_ANKLE, LandmarkPosition.RIGHT_ANKLE,
            LandmarkPosition.LEFT_HEEL, LandmarkPosition.RIGHT_HEEL,
            LandmarkPosition.LEFT_FOOT_INDEX, LandmarkPosition.RIGHT_FOOT_INDEX
        }

        landmarkPairs = [(LandmarkPosition.LEFT_SHOULDER, LandmarkPosition.RIGHT_SHOULDER),
                         (LandmarkPosition.LEFT_SHOULDER, LandmarkPosition.LEFT_HIP),
                         (LandmarkPosition.RIGHT_SHOULDER, LandmarkPosition.RIGHT_HIP),
                         (LandmarkPosition.LEFT_SHOULDER, LandmarkPosition.LEFT_ELBOW),
                         (LandmarkPosition.RIGHT_SHOULDER, LandmarkPosition.RIGHT_ELBOW),
                         (LandmarkPosition.LEFT_ELBOW, LandmarkPosition.LEFT_WRIST),
                         (LandmarkPosition.RIGHT_ELBOW, LandmarkPosition.RIGHT_WRIST),
                         (LandmarkPosition.LEFT_HIP, LandmarkPosition.RIGHT_HIP),
                         (LandmarkPosition.LEFT_HIP, LandmarkPosition.LEFT_KNEE),
                         (LandmarkPosition.RIGHT_HIP, LandmarkPosition.RIGHT_KNEE),
                         (LandmarkPosition.LEFT_KNEE, LandmarkPosition.LEFT_ANKLE),
                         (LandmarkPosition.RIGHT_KNEE, LandmarkPosition.RIGHT_ANKLE),
                         (LandmarkPosition.LEFT_ANKLE, LandmarkPosition.LEFT_HEEL),
                         (LandmarkPosition.RIGHT_ANKLE, LandmarkPosition.RIGHT_HEEL),
                         (LandmarkPosition.LEFT_HEEL, LandmarkPosition.LEFT_FOOT_INDEX),
                         (LandmarkPosition.RIGHT_HEEL, LandmarkPosition.RIGHT_FOOT_INDEX),
                         (LandmarkPosition.LEFT_ANKLE, LandmarkPosition.LEFT_FOOT_INDEX),
                         (LandmarkPosition.RIGHT_ANKLE, LandmarkPosition.RIGHT_FOOT_INDEX)]

        landmarkPositions = {}
        for measurement in frameMeasurement.measurements:
            if measurement.landmark in landmarksToDraw:
                pos = (
                    int(measurement.x * self.activeFrame.shape[1]),
                    int(measurement.y * self.activeFrame.shape[0])
                )
                cv2.circle(self.activeFrame, pos, 5, (0, 255, 50), -1)
                landmarkPositions[measurement.landmark] = pos

        for (landmark1, landmark2) in landmarkPairs:
            if landmark1 in landmarkPositions and landmark2 in landmarkPositions:
                cv2.line(self.activeFrame, landmarkPositions[landmark1],
                         landmarkPositions[landmark2], (255, 255, 255), 2)

>>>>>>> master
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

<<<<<<< HEAD
    def displayResult(self, stateText):
        self.stateText = f'Is on rowing machine: {stateText}'
=======
    def displayResult(self, feedbackMessage):
        self.feedbackMessage = f'Feedback on previous state: {feedbackMessage}'
>>>>>>> master

    def displayDrivePhaseChecker(self, stateText):
        self.stateText = f'Current State: {stateText}'

    def show(self):
        # The counter should be shown on every frame, so we draw it here and track it in the class
        if self.count is not None:
            # Big white text in top left corner
            cv2.putText(self.activeFrame, str(self.count), (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (255, 255, 255), 4, cv2.LINE_AA)

<<<<<<< HEAD
        # Show the text for displaying state of IsOnRowingMachineChecker
        if self.stateText is not None:
            stateText = str(self.stateText)
            cv2.putText(self.activeFrame, stateText, (10, 100), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (55, 55, 255), 4, cv2.LINE_AA)
=======
        if self.stateText is not None or self.feedbackMessage is not None:
            stateText = str(self.stateText)
            feedbackMessage = str(self.feedbackMessage)

            wrappedStateText = textwrap.wrap(stateText,
                                             width=60)  # split stateText into multiple lines if it's too long
            wrappedFeedbackMessage = textwrap.wrap(feedbackMessage,
                                                   width=60)  # split feedbackMessage into multiple lines if it's too long

            yTextStart = 40  # initial y position for text
            for i, line in enumerate(wrappedStateText):
                y = yTextStart + i * 20  # adjust 20 according to your font size
                cv2.putText(self.activeFrame, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (250, 50, 250), 2,
                            cv2.LINE_AA)
            yTextStart = 80  # adjust this according to your needs
            for i, line in enumerate(wrappedFeedbackMessage):
                y = yTextStart + i * 40  # adjust 20 according to your font size
                cv2.putText(self.activeFrame, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (15, 255, 15), 2,
                            cv2.LINE_AA)
>>>>>>> master

        # Show the frame
        if self.activeFrame is not None:
            cv2.imshow(self.windowName, self.activeFrame)
            self.activeFrame = None

    # Close the window
    def close(self):
        cv2.destroyAllWindows()
