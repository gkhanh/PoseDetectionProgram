import cv2
import mediapipe as mp

from src.entity.Measurement import Measurement
from src.entity.PoseData import PoseData
from src.exception.EmptyFrameException import EmptyFrameException
from src.exception.ImageProcessingException import ImageProcessingException
from src.exception.VideoOpenException import VideoOpenException
from src.utils.VideoReader import VideoReader

videoReader = VideoReader('D:/MoveLabStudio/Assignment/PoseDetectionPrototype/resources/video2.mp4')

# Threshold values for recognizing objects
VISIBILITY_THRESHOLD = 0.5
PRESENCE_THRESHOLD = 0.5


def exitProgramWhenButtonPressed(quitButton='q') -> None:
    if cv2.waitKey(1) & 0xFF == ord(quitButton):
        exit(0)


class PoseDetector:
    def __init__(self) -> None:
        self.listener = None
        self.frameNumber = 0
        self.previousKeypoints = None
        self.timestamp = videoReader.getTimeStamp()
        self.mpPose = mp.solutions.pose
        self.mpDrawing = mp.solutions.drawing_utils
        self.pose = self.mpPose.Pose()

    @staticmethod
    def applyLowpassFilter(poseData: PoseData, keypoints: list, alpha: float = 0.5) -> list:
        landmarks = poseData.pose_world_landmarks.landmark
        # Design the low-pass filter
        for i, landmark in enumerate(landmarks):
            landmark.x = round((alpha * landmark.x + (1 - alpha) * keypoints[i].x),
                               3)
            landmark.y = round((alpha * landmark.y + (1 - alpha) * keypoints[i].y),
                               3)
            landmark.z = round((alpha * landmark.z + (1 - alpha) * keypoints[i].z),
                               3)
        return landmarks

    def run(self) -> list:
        if not videoReader.openedVideo():
            errorOpeningVideoMessage = "Error opening video stream or file"
            raise VideoOpenException(errorOpeningVideoMessage)
        frameMeasurements = []
        while videoReader.openedVideo():
            self.timestamp = videoReader.getTimeStamp()
            frame = videoReader.readFrame()
            ret = videoReader.videoCapture.read()

            if not ret:
                imageProcessingErrorMessage = "Error processing images (maybe stream end?)"
                raise ImageProcessingException(imageProcessingErrorMessage)

            if not videoReader.isUsingCamera and frame is None:
                print("Video ended")
                break

            frameMeasurements.append(self.processFrame(frame))
            exitProgramWhenButtonPressed()
            self.frameNumber += 1

            windowName = "MediaPipe Pose"
            cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
            cv2.imshow(windowName, frame)

        videoReader.release()
        cv2.destroyAllWindows()

        measurements = []
        for frameMeasurement in frameMeasurements:
            for measurement in frameMeasurement:
                measurements.append(measurement)

        return measurements

    def processFrame(self, frame):
        if frame is None:
            raise EmptyFrameException("This should not happen")
        frameMeasurement = []
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # result.pose_landmarks and result.pose_world_landmarks should contain landmarks
        # landmark contains x,y,z
        result = self.pose.process(frameRGB)

        poseData = PoseData(pose_landmarks=result.pose_landmarks,
                            pose_world_landmarks=result.pose_world_landmarks,
                            segmentation_mask=result.segmentation_mask)

        if result is not None and result.pose_landmarks:
            self.previousKeypoints = poseData.pose_world_landmarks.landmark if self.previousKeypoints is None else self.previousKeypoints
            self.mpDrawing.draw_landmarks(frame, poseData.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
            self.previousKeypoints = self.applyLowpassFilter(poseData, self.previousKeypoints)
            dataToWrite = self.extractPoseCoordinatesFromLandmark(poseData)
            frameMeasurement = self.convertRawdataToMeasurementObjectForSquatPosture(dataToWrite)

        return frameMeasurement

    def extractPoseCoordinatesFromLandmark(self, poseData: PoseData) -> tuple:
        landmarks = poseData.pose_world_landmarks.landmark
        # Create a class that contains all of these data
        # Get coordinates
        ankle = [landmarks[self.mpPose.PoseLandmark.RIGHT_ANKLE.value].x,
                 landmarks[self.mpPose.PoseLandmark.RIGHT_ANKLE.value].y,
                 landmarks[self.mpPose.PoseLandmark.RIGHT_ANKLE.value].z]
        shoulder = [landmarks[self.mpPose.PoseLandmark.RIGHT_SHOULDER.value].x,
                    landmarks[self.mpPose.PoseLandmark.RIGHT_SHOULDER.value].y,
                    landmarks[self.mpPose.PoseLandmark.RIGHT_SHOULDER.value].z]
        elbow = [landmarks[self.mpPose.PoseLandmark.LEFT_ELBOW.value].x,
                 landmarks[self.mpPose.PoseLandmark.LEFT_ELBOW.value].y,
                 landmarks[self.mpPose.PoseLandmark.LEFT_ELBOW.value].z]
        wrist = [landmarks[self.mpPose.PoseLandmark.LEFT_WRIST.value].x,
                 landmarks[self.mpPose.PoseLandmark.LEFT_WRIST.value].y,
                 landmarks[self.mpPose.PoseLandmark.LEFT_WRIST.value].z]
        hip = [landmarks[self.mpPose.PoseLandmark.RIGHT_HIP.value].x,
               landmarks[self.mpPose.PoseLandmark.RIGHT_HIP.value].y,
               landmarks[self.mpPose.PoseLandmark.RIGHT_HIP.value].z]
        knee = [landmarks[self.mpPose.PoseLandmark.RIGHT_KNEE.value].x,
                landmarks[self.mpPose.PoseLandmark.RIGHT_KNEE.value].y,
                landmarks[self.mpPose.PoseLandmark.RIGHT_KNEE.value].z]
        return hip, knee

    def convertRawdataToMeasurementObjectForAllData(self, landmarks):
        measurements = []
        for index, landmark in enumerate(landmarks):
            measurement = Measurement(self.timestamp,
                                      self.mpPose.PoseLandmark(index).name,
                                      landmark.x,
                                      landmark.y,
                                      landmark.z)
            measurements.append(measurement)
        return measurements

    def convertRawdataToMeasurementObjectForSquatPosture(self, landmarks):
        measurements = []
        hip, knee = landmarks
        measurementHip = Measurement(self.timestamp,
                                     self.mpPose.PoseLandmark.RIGHT_HIP.name,
                                     hip[0],
                                     hip[1],
                                     hip[2])
        measurementKnee = Measurement(self.timestamp,
                                      self.mpPose.PoseLandmark.RIGHT_KNEE.name,
                                      knee[0],
                                      knee[1],
                                      knee[2])
        measurements.append(measurementHip)
        measurements.append(measurementKnee)
        return measurements
