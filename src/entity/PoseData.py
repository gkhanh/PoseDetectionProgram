from dataclasses import dataclass
from typing import Optional

#Class to contain NamedTuple from mediapipe pose.process
@dataclass
class PoseData:
    pose_landmarks: list
    pose_world_landmarks: list
    segmentation_mask: Optional[list] = None
