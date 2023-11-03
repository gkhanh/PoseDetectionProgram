import cv2
import mediapipe as mp
from scipy import signal

from src.entity.PoseData import PoseData
from src.exception.EmptyFrameException import EmptyFrameException
from src.exception.VideoOpenException import VideoOpenException
from src.exception.ImageProcessingException import ImageProcessingException
from src.utils.VideoReader import VideoReader

# Threshold values for recognizing objects
VISIBILITY_THRESHOLD = 0.5
PRESENCE_THRESHOLD = 0.5

mpPose = mp.solutions.pose


class PoseDetector:
    def __init__(self, listener) -> None:
        self.listener = listener
        self.frameNumber = 0
        self.previousKeypoints = None
        self.mpPose = mp.solutions.pose
        self.mpDrawing = mp.solutions.drawing_utils
        self.pose = mpPose.Pose()

    def runPoseCheckerWrapper(self, videoPath='./resources/video2.mp4') -> None:
        videoReader = VideoReader(videoPath)
        self.runPoseChecker(videoReader)

    # Refactor candidate to move to other class/file
    def applyLowpassFilter(self, poseData: PoseData, alpha: float = 0.5) -> list:
        landmarks = poseData.pose_world_landmarks.landmark

        # Design the low-pass filter
        coefficients = signal.butter(4, alpha, 'low', analog=False)
        b = coefficients[0]
        a = coefficients[1]

        for i, landmark in enumerate(landmarks):
            # Apply the low-pass filter to each coordinate
            landmark.x = signal.lfilter(b, a, [landmark.x])[0]
            landmark.y = signal.lfilter(b, a, [landmark.y])[0]
            landmark.z = signal.lfilter(b, a, [landmark.z])[0]
        return landmarks

    def runPoseChecker(self, videoReader: VideoReader) -> None:
        if not videoReader.openedVideo():
            errorOpeningVideoMessage = "Error opening video stream or file"
            raise VideoOpenException(errorOpeningVideoMessage)

        while videoReader.openedVideo():
            frame = videoReader.readFrame()
            ret = videoReader.videoCapture.read()

            if not ret:
                imageProcessingErrorMessage = "Error processing images (maybe stream end?)"
                raise ImageProcessingException(imageProcessingErrorMessage)

            if frame is None:
                frameEmptyExceptionMessage = "Frame empty! (maybe stream end?)"
                raise EmptyFrameException(frameEmptyExceptionMessage)

            if frame is not None:
                frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # result.pose_landmarks and result.pose_world_landmarks should contain landmarks
                # landmark contains x,y,z
                result = self.pose.process(frameRGB)

                poseData = PoseData(pose_landmarks=result.pose_landmarks,
                                    pose_world_landmarks=result.pose_world_landmarks,
                                    segmentation_mask=result.segmentation_mask)

                if result is not None and result.pose_landmarks:
                    self.previousKeypoints = poseData.pose_world_landmarks.landmark if self.previousKeypoints is None else self.previousKeypoints

                    self.previousKeypoints = self.applyLowpassFilter(poseData, self.previousKeypoints)

                    self.mpDrawing.draw_landmarks(frame, result.pose_landmarks, mpPose.POSE_CONNECTIONS)

                    self.notifyListener(result.pose_landmarks.landmark)

                    # self.extractPoseCoordinatesFromLandmark(poseData)

                cv2.namedWindow('MediaPipe Pose', cv2.WINDOW_NORMAL)
                cv2.imshow('MediaPipe Pose', frame)

            self.exitProgramWhenButtonPressed()
            self.frameNumber += 1

        videoReader.release()
        cv2.destroyAllWindows()

    def extractPoseCoordinatesFromLandmark(self, poseData: PoseData) -> None:
        landmarks = poseData.pose_world_landmarks.landmark
        # Create a class that contains all of these data
        # Get coordinates
        shoulder = [landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value].x,
                    landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value].y,
                    landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value].z]
        elbow = [landmarks[mpPose.PoseLandmark.LEFT_ELBOW.value].x,
                 landmarks[mpPose.PoseLandmark.LEFT_ELBOW.value].y,
                 landmarks[mpPose.PoseLandmark.LEFT_ELBOW.value].z]
        wrist = [landmarks[mpPose.PoseLandmark.LEFT_WRIST.value].x,
                 landmarks[mpPose.PoseLandmark.LEFT_WRIST.value].y,
                 landmarks[mpPose.PoseLandmark.LEFT_WRIST.value].z]
        hip = [landmarks[mpPose.PoseLandmark.RIGHT_HIP.value].x,
               landmarks[mpPose.PoseLandmark.RIGHT_HIP.value].y,
               landmarks[mpPose.PoseLandmark.RIGHT_HIP.value].z]
        knee = [landmarks[mpPose.PoseLandmark.RIGHT_KNEE.value].x,
                landmarks[mpPose.PoseLandmark.RIGHT_KNEE.value].y,
                landmarks[mpPose.PoseLandmark.RIGHT_KNEE.value].z]
        ankle = [landmarks[mpPose.PoseLandmark.RIGHT_ANKLE.value].x,
                 landmarks[mpPose.PoseLandmark.RIGHT_ANKLE.value].y,
                 landmarks[mpPose.PoseLandmark.RIGHT_ANKLE.value].z]

    def exitProgramWhenButtonPressed(self, quitButton='q') -> None:
        if cv2.waitKey(1) & 0xFF == ord(quitButton):
            exit(0)

    def notifyListener(self, landmarks):
        for idx, landmark in enumerate(landmarks):
            measurement = [
                self.frameNumber,
                self.mpPose.PoseLandmark(idx).name,
                landmark.x,
                landmark.y,
                landmark.z
            ]
            self.listener(measurement)
        return self.listener
