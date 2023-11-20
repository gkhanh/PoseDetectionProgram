from dataclasses import dataclass
from typing import Optional

import numpy as np
import cv2
import mediapipe as mp

from src.exception.VideoOpenException import VideoOpenException
from src.models.FrameMeasurement import FrameMeasurement
from src.models.measurement import Measurement, LandmarkPosition
from src.utils.CalculatedAngles import CalculatedAngles


# This class is used for drawing and extract landmark from video frame
class PoseDetector:
    def __init__(self, videoReader, previewer, listener) -> None:
        self.videoReader = videoReader
        self.previewer = previewer
        self.listener = listener
        self.mpPose = mp.solutions.pose
        self.mpDrawing = mp.solutions.drawing_utils
        self.pose = self.mpPose.Pose()

    def run(self) -> list:
        if not self.videoReader.isOpened():
            raise VideoOpenException("Error opening video stream or file")

        frameMeasurements = []
        self.previewer.open()

        while self.videoReader.isOpened():
            timestamp = self.videoReader.getTimeStamp()
            frame = self.videoReader.readFrame()
            if not self.videoReader.isUsingCamera and frame is None:
                break

            processedFrame = self.processFrame(timestamp, frame)
            frameMeasurements.append(processedFrame)
            self.notifyListener(processedFrame)
            self.previewer.draw(frame)
            self.previewer.wait()

        self.videoReader.release()
        self.previewer.close()

        # Flattening of all measurements
        measurements = []
        for frameMeasurement in frameMeasurements:
            for measurement in frameMeasurement:
                frameMeasurement.append(measurement)

        return frameMeasurements

    def processFrame(self, timestamp, frame):
        frameMeasurement = []
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # result.pose_landmarks and result.pose_world_landmarks should contain landmarks
        # landmark contains x,y,z
        result = self.pose.process(frameRGB)

        poseData = PoseDetector.PoseData(
            pose_landmarks=result.pose_landmarks,
            pose_world_landmarks=result.pose_world_landmarks,
            segmentation_mask=result.segmentation_mask
        )

        if result is not None and result.pose_landmarks:
            self.mpDrawing.draw_landmarks(frame, poseData.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
            frameMeasurement = self.extractPoseCoordinatesFromLandmarkForLeftSide(timestamp, poseData)
        return frameMeasurement

    def extractPoseCoordinatesFromLandmarkForLeftSide(self, timestamp, poseData):
        leftSideLandmarks = poseData.pose_world_landmarks.landmark
        leftShoulder = Measurement(
            timestamp,
            LandmarkPosition.LEFT_SHOULDER,
            leftSideLandmarks[self.mpPose.PoseLandmark.LEFT_SHOULDER.value].x,
            leftSideLandmarks[self.mpPose.PoseLandmark.LEFT_SHOULDER.value].y,
            leftSideLandmarks[self.mpPose.PoseLandmark.LEFT_SHOULDER.value].z,
        )
        leftElbow = Measurement(
            timestamp,
            LandmarkPosition.LEFT_ELBOW,
            leftSideLandmarks[self.mpPose.PoseLandmark.LEFT_ELBOW.value].x,
            leftSideLandmarks[self.mpPose.PoseLandmark.LEFT_ELBOW.value].y,
            leftSideLandmarks[self.mpPose.PoseLandmark.LEFT_ELBOW.value].z
        )
        leftHip = Measurement(
            timestamp,
            LandmarkPosition.LEFT_HIP,
            leftSideLandmarks[self.mpPose.PoseLandmark.LEFT_HIP.value].x,
            leftSideLandmarks[self.mpPose.PoseLandmark.LEFT_HIP.value].y,
            leftSideLandmarks[self.mpPose.PoseLandmark.LEFT_HIP.value].z
        )
        leftKnee = Measurement(
            timestamp,
            LandmarkPosition.LEFT_KNEE,
            leftSideLandmarks[self.mpPose.PoseLandmark.LEFT_KNEE.value].x,
            leftSideLandmarks[self.mpPose.PoseLandmark.LEFT_KNEE.value].y,
            leftSideLandmarks[self.mpPose.PoseLandmark.LEFT_KNEE.value].z
        )
        leftAnkle = Measurement(
            timestamp,
            LandmarkPosition.LEFT_ANKLE,
            leftSideLandmarks[self.mpPose.PoseLandmark.LEFT_ANKLE.value].x,
            leftSideLandmarks[self.mpPose.PoseLandmark.LEFT_ANKLE.value].y,
            leftSideLandmarks[self.mpPose.PoseLandmark.LEFT_ANKLE.value].z
        )
        return FrameMeasurement(timestamp, [leftShoulder, leftElbow, leftHip, leftKnee, leftAnkle])

    def extractPoseCoordinatesFromLandmarkForRightSide(self, timestamp, poseData):
        rightSideLandmarks = poseData.pose_world_landmarks.landmark
        rightShoulder = Measurement(
            timestamp,
            LandmarkPosition.RIGHT_SHOULDER,
            rightSideLandmarks[self.mpPose.PoseLandmark.RIGHT_SHOULDER.value].x,
            rightSideLandmarks[self.mpPose.PoseLandmark.RIGHT_SHOULDER.value].y,
            rightSideLandmarks[self.mpPose.PoseLandmark.RIGHT_SHOULDER.value].z,
        )
        rightElbow = Measurement(
            timestamp,
            LandmarkPosition.RIGHT_ELBOW,
            rightSideLandmarks[self.mpPose.PoseLandmark.RIGHT_ELBOW.value].x,
            rightSideLandmarks[self.mpPose.PoseLandmark.RIGHT_ELBOW.value].y,
            rightSideLandmarks[self.mpPose.PoseLandmark.RIGHT_ELBOW.value].z
        )
        rightHip = Measurement(
            timestamp,
            LandmarkPosition.RIGHT_HIP,
            rightSideLandmarks[self.mpPose.PoseLandmark.RIGHT_HIP.value].x,
            rightSideLandmarks[self.mpPose.PoseLandmark.RIGHT_HIP.value].y,
            rightSideLandmarks[self.mpPose.PoseLandmark.RIGHT_HIP.value].z
        )
        rightKnee = Measurement(
            timestamp,
            LandmarkPosition.RIGHT_KNEE,
            rightSideLandmarks[self.mpPose.PoseLandmark.RIGHT_KNEE.value].x,
            rightSideLandmarks[self.mpPose.PoseLandmark.RIGHT_KNEE.value].y,
            rightSideLandmarks[self.mpPose.PoseLandmark.RIGHT_KNEE.value].z
        )
        rightAnkle = Measurement(
            timestamp,
            LandmarkPosition.RIGHT_ANKLE,
            rightSideLandmarks[self.mpPose.PoseLandmark.RIGHT_ANKLE.value].x,
            rightSideLandmarks[self.mpPose.PoseLandmark.RIGHT_ANKLE.value].y,
            rightSideLandmarks[self.mpPose.PoseLandmark.RIGHT_ANKLE.value].z
        )
        return FrameMeasurement(timestamp,[rightShoulder, rightElbow, rightHip, rightKnee, rightAnkle])

    def notifyListener(self, frameMeasurement):
        self.listener.onMeasurement(frameMeasurement)

    @dataclass
    class PoseData:
        pose_landmarks: list
        pose_world_landmarks: list
        segmentation_mask: Optional[list] = None

    class Listener:

        def onMeasurement(self, measurement: Measurement):
            pass
