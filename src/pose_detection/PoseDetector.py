from dataclasses import dataclass
from typing import Optional

import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision.core.vision_task_running_mode import VisionTaskRunningMode

from src.exception.VideoOpenException import VideoOpenException
from src.models.FrameMeasurement import FrameMeasurement
from src.models.measurement import Measurement, LandmarkPosition


# Reference material: https://github.com/googlesamples/mediapipe/blob/main/examples/pose_landmarker/python/%5BMediaPipe_Python_Tasks%5D_Pose_Landmarker.ipynb

# This class is used for drawing and extract landmark from video frame
class PoseDetector:
    def __init__(self, videoReader, previewer, listener) -> None:
        self.videoReader = videoReader
        self.previewer = previewer
        self.listener = listener
        self.pose = self.createPoseDetector()

    def createPoseDetector(self):
        base_options = python.BaseOptions(
            model_asset_path='./src/pose_landmarker_heavy.task',
        )
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=VisionTaskRunningMode.VIDEO,
            num_poses=1,
            min_tracking_confidence=0.70,
            min_pose_detection_confidence=0.70,
            min_pose_presence_confidence=0.70
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

            frameMeasurement = self.processFrame(timestamp, frame)
            self.notifyListener(frameMeasurement)
            self.previewer.draw(frame)
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

        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in
            poseData.pose_landmarks
        ])
        mp.solutions.drawing_utils.draw_landmarks(
            frame,
            pose_landmarks_proto,
            mp.solutions.pose.POSE_CONNECTIONS,
            mp.solutions.drawing_styles.get_default_pose_landmarks_style()
        )
        return self.extractPoseCoordinatesFromLandmark(timestamp, poseData)

    def extractPoseCoordinatesFromLandmark(self, timestamp, poseData):
        landmarks = poseData.pose_world_landmarks
        positions = [
            LandmarkPosition.NOSE,
            LandmarkPosition.LEFT_EYE_INNER,
            LandmarkPosition.LEFT_EYE,
            LandmarkPosition.LEFT_EYE_OUTER,
            LandmarkPosition.LEFT_EAR,
            LandmarkPosition.MOUTH_LEFT,
            LandmarkPosition.LEFT_SHOULDER,
            LandmarkPosition.LEFT_ELBOW,
            LandmarkPosition.LEFT_WRIST,
            LandmarkPosition.LEFT_PINKY,
            LandmarkPosition.LEFT_INDEX,
            LandmarkPosition.LEFT_THUMB,
            LandmarkPosition.LEFT_HIP,
            LandmarkPosition.LEFT_KNEE,
            LandmarkPosition.LEFT_ANKLE,
            LandmarkPosition.LEFT_HEEL,
            LandmarkPosition.LEFT_FOOT_INDEX,
            LandmarkPosition.RIGHT_EYE_INNER,
            LandmarkPosition.RIGHT_EYE,
            LandmarkPosition.RIGHT_EYE_OUTER,
            LandmarkPosition.RIGHT_EAR,
            LandmarkPosition.MOUTH_RIGHT,
            LandmarkPosition.RIGHT_SHOULDER,
            LandmarkPosition.RIGHT_ELBOW,
            LandmarkPosition.RIGHT_WRIST,
            LandmarkPosition.RIGHT_PINKY,
            LandmarkPosition.RIGHT_INDEX,
            LandmarkPosition.RIGHT_THUMB,
            LandmarkPosition.RIGHT_HIP,
            LandmarkPosition.RIGHT_KNEE,
            LandmarkPosition.RIGHT_ANKLE,
            LandmarkPosition.RIGHT_HEEL,
            LandmarkPosition.RIGHT_FOOT_INDEX
        ]
        measurements = []
        for position in positions:
            landmark = landmarks[getattr(mp.solutions.pose.PoseLandmark, position.name).value]
            measurement = Measurement(timestamp, position, landmark.x, landmark.y, landmark.z)
            measurements.append(measurement)
        return FrameMeasurement(timestamp, measurements)

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
