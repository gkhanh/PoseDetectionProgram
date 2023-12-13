from dataclasses import dataclass
from enum import Enum


class NormalizedLandmarkPosition(Enum):
    SHOULDER = "SHOULDER"
    ELBOW = "ELBOW"
    WRIST = "WRIST"
    PINKY = "PINKY"
    INDEX = "INDEX"
    THUMB = "THUMB"
    HIP = "HIP"
    KNEE = "KNEE"
    ANKLE = "ANKLE"
    HEEL = "HEEL"
    FOOT_INDEX = "FOOT_INDEX"
    EYE = "EYE"
    EAR = "EAR"
    EYE_INNER = "EYE_INNER"
    EYE_OUTER = "EYE_OUTER"


@dataclass
class NormalizedMeasurement:
    timestamp: float
    landmark: NormalizedLandmarkPosition
    x: float
    y: float
    z: float
