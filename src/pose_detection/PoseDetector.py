from dataclasses import dataclass
from typing import Optional

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision.core.vision_task_running_mode import VisionTaskRunningMode

from src.exception.VideoOpenException import VideoOpenException
from src.models.FrameMeasurement import FrameMeasurement
from src.models.Measurement import Measurement, LandmarkPosition
from src.utils.Cancellable import Cancellable


# Reference material: https://github.com/googlesamples/mediapipe/blob/main/examples/pose_landmarker/python/%5BMediaPipe_Python_Tasks%5D_Pose_Landmarker.ipynb

# This class is used for drawing and extract landmark from video frame
class PoseDetector:
    def __init__(self, videoReader, previewer) -> None:
        self.videoReader = videoReader
        self.previewer = previewer
        self.pose = self.createPoseDetector()

        self.listeners = []

    def addListener(self, listener):
        self.listeners.append(listener)

        return Cancellable(lambda: self.listeners.remove(listener))

    def createPoseDetector(self):
        # Choose the lite model for smoother and faster video processing
        base_options = python.BaseOptions(
            model_asset_path='./src/pose_landmarker_heavy.task',
            # model_asset_path='./src/pose_landmarker_lite.task'
        )
        # For smoother video set the value to 0.7 or higher
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=VisionTaskRunningMode.VIDEO,
            num_poses=1,
            min_tracking_confidence=0.60,
            min_pose_detection_confidence=0.60,
            min_pose_presence_confidence=0.60
        )
        return vision.PoseLandmarker.create_from_options(options)

    def run(self):
        if not self.videoReader.isOpened():
            raise VideoOpenException("Error opening video stream or file")
        self.previewer.open()

        while self.videoReader.isOpened():
            frame = self.videoReader.readFrame()
            timestamp = self.videoReader.getTimeStamp()
            if not self.videoReader.isUsingCamera and frame is None:
                break

            self.previewer.changeFrame(frame)

            frameMeasurement = self.processFrame(timestamp, frame)
            if frameMeasurement is not None:
                self.notifyListener(frameMeasurement)
            self.previewer.show()
            self.previewer.wait()

        self.videoReader.release()
        self.previewer.close()

    def processFrame(self, timestamp, frame):
        result = self.pose.detect_for_video(
            mp.Image(image_format=mp.ImageFormat.SRGB, data=frame),
            int(timestamp)
        )

        if result is None or len(result.pose_landmarks) == 0 or len(result.pose_world_landmarks) == 0:
            return

        poseData = PoseDetector.PoseData(
            pose_landmarks=result.pose_landmarks[0],
            pose_world_landmarks=result.pose_world_landmarks[0]
        )

        self.previewer.drawLandmarks(poseData.pose_landmarks)

        return self.extractPoseCoordinatesFromLandmark(timestamp, poseData)

    def extractPoseCoordinatesFromLandmark(self, timestamp, poseData):
        landmarks = poseData.pose_landmarks

        # Get all PoseLandmark enum members
        positions = list(LandmarkPosition.__members__.values())

        # Create measurements using list comprehension
        measurements = [Measurement(timestamp, position,
                                    landmarks[idx].x,
                                    landmarks[idx].y,
                                    landmarks[idx].z) for idx, position in enumerate(positions)]

        return FrameMeasurement(timestamp, measurements)

    def notifyListener(self, frameMeasurement):
        for listener in self.listeners:
            listener.onMeasurement(frameMeasurement)

    @dataclass
    class PoseData:
        pose_landmarks: list
        pose_world_landmarks: list
        segmentation_mask: Optional[list] = None

    # Listener class
    class Listener:

        def onMeasurement(self, frameMeasurement: FrameMeasurement):
            raise NotImplementedError
