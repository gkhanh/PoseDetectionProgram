from dataclasses import dataclass
from enum import Enum


class LandmarkPosition(Enum):
    NOSE = "NOSE"  # 0
    LEFT_EYE_INNER = "LEFT_EYE_INNER"  # 1
    LEFT_EYE = "LEFT_EYE"  # 2
    LEFT_EYE_OUTER = "LEFT_EYE_OUTER"  # 3
    RIGHT_EYE_INNER = "RIGHT_EYE_INNER"  # 4
    RIGHT_EYE = "RIGHT_EYE"  # 5
    RIGHT_EYE_OUTER = "RIGHT_EYE_OUTER"  # 6
    LEFT_EAR = "LEFT_EAR"  # 7
    RIGHT_EAR = "RIGHT_EAR"  # 8
    MOUTH_LEFT = "MOUTH_LEFT"  # 9
    MOUTH_RIGHT = "MOUTH_RIGHT"  # 10
    LEFT_SHOULDER = "LEFT_SHOULDER"  # 11
    RIGHT_SHOULDER = "RIGHT_SHOULDER"  # 12
    LEFT_ELBOW = "LEFT_ELBOW"  # 13
    RIGHT_ELBOW = "RIGHT_ELBOW"  # 14
    LEFT_WRIST = "LEFT_WRIST"  # 15
    RIGHT_WRIST = "RIGHT_WRIST"  # 16
    LEFT_PINKY = "LEFT_PINKY"  # 17
    RIGHT_PINKY = "RIGHT_PINKY"  # 18
    LEFT_INDEX = "LEFT_INDEX"  # 19
    RIGHT_INDEX = "RIGHT_INDEX"  # 20
    LEFT_THUMB = "LEFT_THUMB"  # 21
    RIGHT_THUMB = "RIGHT_THUMB"  # 22
    LEFT_HIP = "LEFT_HIP"  # 23
    RIGHT_HIP = "RIGHT_HIP"  # 24
    LEFT_KNEE = "LEFT_KNEE"  # 25
    RIGHT_KNEE = "RIGHT_KNEE"  # 26
    LEFT_ANKLE = "LEFT_ANKLE"  # 27
    RIGHT_ANKLE = "RIGHT_ANKLE"  # 28
    LEFT_HEEL = "LEFT_HEEL"  # 29
    RIGHT_HEEL = "RIGHT_HEEL"  # 30
    LEFT_FOOT_INDEX = "LEFT_FOOT_INDEX"  # 31
    RIGHT_FOOT_INDEX = "RIGHT_FOOT_INDEX"  # 32


@dataclass
class Measurement:
    # frameNumber: int
    timestamp: float
    landmark: LandmarkPosition
    x: float
    y: float
    z: float
