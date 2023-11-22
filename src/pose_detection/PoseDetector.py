from dataclasses import dataclass
from typing import Optional

import numpy as np
import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import ObjectDetector, ObjectDetectorOptions
from mediapipe.tasks.python.vision.core.vision_task_running_mode import VisionTaskRunningMode

from src.exception.VideoOpenException import VideoOpenException
from src.models.FrameMeasurement import FrameMeasurement
from src.models.measurement import Measurement, LandmarkPosition
from src.utils.CalculatedAngles import CalculatedAngles
from src.utils.VideoReader import VideoReader


# This class is used for drawing and extract landmark from video frame
class PoseDetector:
    def __init__(self, videoReader, previewer, listener) -> None:
        self.videoReader = videoReader
        self.previewer = previewer
        self.listener = listener
        # self.pose = mp.solutions.pose.Pose()
        self.pose = self.createPoseDetector()


    def createPoseDetector(self):
        base_options = python.BaseOptions(
            model_asset_path='D:/MoveLabStudio/Assignment/PoseDetection-Prototype/src/pose_landmarker_heavy.task',
        )
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=VisionTaskRunningMode.VIDEO,
            num_poses=1,
            min_tracking_confidence=0.95,
            min_pose_detection_confidence=0.95,
            min_pose_presence_confidence=0.95
        )
        return vision.PoseLandmarker.create_from_options(options)

    def run(self):
        if not self.videoReader.isOpened():
            raise VideoOpenException("Error opening video stream or file")
        self.previewer.open()

        while self.videoReader.isOpened():
            timestamp = self.videoReader.getTimeStamp()
            frame = self.videoReader.readFrame()
            if not self.videoReader.isUsingCamera and frame is None:
                break

            frameMeasurement = self.processFrame(timestamp, frame)
            self.notifyListener(frameMeasurement)
            self.previewer.draw(frame)
            self.previewer.wait()

        self.videoReader.release()
        self.previewer.close()

    def processFrame(self, timestamp, frame):
        frameMeasurementList = []
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # preProcessedResult = self.pose.process(frameRGB)

        result = self.pose.detect_for_video(
            mp.Image(image_format=mp.ImageFormat.SRGB, data=frame),
            int(timestamp)
        )

        if result is None or len(result.pose_landmarks) == 0:
            return

        poseData = PoseDetector.PoseData(
            pose_landmarks=result.pose_landmarks,
            pose_world_landmarks=result.pose_world_landmarks
        )

        if result is not None and result.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, poseData.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
            frameMeasurementList = self.extractPoseCoordinatesFromLandmark(timestamp, poseData)

        return frameMeasurementList

    def extractPoseCoordinatesFromLandmark(self, timestamp, poseData):
        Landmarks = poseData.pose_world_landmarks.landmark
        leftShoulder = Measurement(
            timestamp,
            LandmarkPosition.LEFT_SHOULDER,
            Landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x,
            Landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y,
            Landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].z,
        )
        leftElbow = Measurement(
            timestamp,
            LandmarkPosition.LEFT_ELBOW,
            Landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].x,
            Landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].y,
            Landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].z
        )
        leftHip = Measurement(
            timestamp,
            LandmarkPosition.LEFT_HIP,
            Landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x,
            Landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y,
            Landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].z
        )
        leftKnee = Measurement(
            timestamp,
            LandmarkPosition.LEFT_KNEE,
            Landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].x,
            Landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].y,
            Landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].z
        )
        leftAnkle = Measurement(
            timestamp,
            LandmarkPosition.LEFT_ANKLE,
            Landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].x,
            Landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].y,
            Landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].z
        )
        rightShoulder = Measurement(
            timestamp,
            LandmarkPosition.RIGHT_SHOULDER,
            Landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x,
            Landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y,
            Landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].z,
        )
        rightElbow = Measurement(
            timestamp,
            LandmarkPosition.RIGHT_ELBOW,
            Landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].x,
            Landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].y,
            Landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].z
        )
        rightHip = Measurement(
            timestamp,
            LandmarkPosition.RIGHT_HIP,
            Landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].x,
            Landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].y,
            Landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].z
        )
        rightKnee = Measurement(
            timestamp,
            LandmarkPosition.RIGHT_KNEE,
            Landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value].x,
            Landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value].y,
            Landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value].z
        )
        rightAnkle = Measurement(
            timestamp,
            LandmarkPosition.RIGHT_ANKLE,
            Landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].x,
            Landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].y,
            Landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].z
        )
        return FrameMeasurement(timestamp,
                                [leftShoulder, leftElbow, leftHip, leftKnee, leftAnkle, rightShoulder, rightElbow,
                                 rightHip, rightKnee, rightAnkle])

    def notifyListener(self, frameMeasurement):
        self.listener.onMeasurement(frameMeasurement)

    @dataclass
    class PoseData:
        pose_landmarks: list
        pose_world_landmarks: list
        segmentation_mask: Optional[list] = None

    # Listener class
    class Listener:

        def onMeasurement(self, measurement: Measurement):
            # Listener to receive results asynchronously
            pass
