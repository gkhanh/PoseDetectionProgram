from src.utils.MathUtils import MathUtils
from src.models.measurement import LandmarkPosition


class CalculatedAngles:
    def __init__(self, measurements) -> None:
        self.measurements = measurements
        self.operation = MathUtils()

    def calculateHipAngle(self):
        lastFrameMeasurement = self.measurements[-1]
        # Find the RIGHT_KNEE
        kneeCoordinates = None
        for measurement in lastFrameMeasurement.measurements:
            if measurement.landmark == LandmarkPosition.RIGHT_KNEE:
                kneeCoordinates = measurement
                break
        if kneeCoordinates is None:
            return None

        # Find the RIGHT_HIP
        hipCoordinates = None
        for measurement in lastFrameMeasurement.measurements:
            if measurement.landmark == LandmarkPosition.RIGHT_HIP:
                hipCoordinates = measurement
                break
        if hipCoordinates is None:
            return None

        # Find the RIGHT_SHOULDER
        shoulderCoordinates = None
        for measurement in lastFrameMeasurement.measurements:
            if measurement.landmark == LandmarkPosition.RIGHT_SHOULDER:
                shoulderCoordinates = measurement
                break
        if shoulderCoordinates is None:
            return None

        hipAngle = self.operation.calculateAngle(
            (shoulderCoordinates.x, shoulderCoordinates.y),
            (hipCoordinates.x, hipCoordinates.y),
            (kneeCoordinates.x, kneeCoordinates.y),
        )
        return round(hipAngle, 2)
