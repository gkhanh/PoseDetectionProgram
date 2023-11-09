from dataclasses import dataclass
from typing import Optional

#Class to contain NamedTuple from mediapipe pose.process
@dataclass
class Measurement:
    # frameNumber: int
    timestamp: float
    landmark: str
    x: float
    y: float
    z: float