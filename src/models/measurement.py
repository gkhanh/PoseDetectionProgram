from dataclasses import dataclass
from enum import Enum


class LandmarkPosition(Enum):
    RIGHT_HIP = "RIGHT_HIP"
    RIGHT_KNEE = "RIGHT_KNEE"


@dataclass
class Measurement:
    # frameNumber: int
    timestamp: float
    landmark: LandmarkPosition
    x: float
    y: float
    z: float
