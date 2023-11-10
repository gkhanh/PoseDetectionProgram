from dataclasses import dataclass
from typing import Optional

import cv2
import mediapipe as mp

from src.exception.VideoOpenException import VideoOpenException
from src.models.measurement import Measurement, LandmarkPosition


class PoseDetector:
    def __init__(self, videoReader, previewer) -> None:
        self.videoReader = videoReader
        self.previewer = previewer
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

            frameMeasurements.append(self.processFrame(timestamp, frame))

            self.previewer.draw(frame)
            self.previewer.wait()

        self.videoReader.release()
        self.previewer.close()

        # Flattening of all measurements
        measurements = []
        for frameMeasurement in frameMeasurements:
            for measurement in frameMeasurement:
                measurements.append(measurement)

        return measurements

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
            frameMeasurement = self.extractPoseCoordinatesFromLandmark(timestamp, poseData)

        return frameMeasurement

    def extractPoseCoordinatesFromLandmark(self, timestamp, poseData) -> list:
        landmarks = poseData.pose_world_landmarks.landmark

        hip = Measurement(
            timestamp,
            LandmarkPosition.RIGHT_HIP,
            landmarks[self.mpPose.PoseLandmark.RIGHT_HIP.value].x,
            landmarks[self.mpPose.PoseLandmark.RIGHT_HIP.value].y,
            landmarks[self.mpPose.PoseLandmark.RIGHT_HIP.value].z
        )
        knee = Measurement(
            timestamp,
            LandmarkPosition.RIGHT_KNEE,
            landmarks[self.mpPose.PoseLandmark.RIGHT_KNEE.value].x,
            landmarks[self.mpPose.PoseLandmark.RIGHT_KNEE.value].y,
            landmarks[self.mpPose.PoseLandmark.RIGHT_KNEE.value].z
        )
        return [hip, knee]

    @dataclass
    class PoseData:
        pose_landmarks: list
        pose_world_landmarks: list
        segmentation_mask: Optional[list] = None
