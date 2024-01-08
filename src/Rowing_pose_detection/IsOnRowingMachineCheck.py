from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData
from src.pose_detection.RowingPoseDetector import RowingPoseDetector
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.models.NormalizedFrameMeasurement import NormalizedFrameMeasurement
from src.utils.Cancellable import Cancellable
from src.utils.MathUtils import MathUtils
from src.exception.EmptyDataException import EmptyDataException


class IsOnRowingMachineCheck(RowingPoseDetector.Listener):
    def __init__(self, rowingPoseDetector) -> None:
        self.rowingPoseDetector = rowingPoseDetector
        self.distance = 0.0
        self.listeners = []
        self.isOnRowingMachine = False
        self.poseDetectorCancellable = None

    def addListener(self, listener):
        self.listeners.append(listener)
        listener.onRowingMachineCheck(self.isOnRowingMachine)

        if len(self.listeners) == 1:
            self.poseDetectorCancellable = self.rowingPoseDetector.addListener(self)

        return Cancellable(lambda: self._removeListener(listener))

    def _removeListener(self, listener):
        self.listeners.remove(listener)
        if len(self.listeners) == 0:
            self.poseDetectorCancellable.cancel()

    def calculateHeelAndHipDistance(self, normalizedFrameMeasurement):
        try:
            distanceCalculator = MathUtils()
            # Find the HEEL
            heelMeasurement = None
            if not normalizedFrameMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in normalizedFrameMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.HEEL:
                    heelMeasurement = normalizedMeasurement
                    break
            if heelMeasurement is None:
                return None

            # Find the RIGHT_HIP
            hipMeasurement = None
            if not normalizedFrameMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in normalizedFrameMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.HIP:
                    hipMeasurement = normalizedMeasurement
                    break
            if hipMeasurement is None:
                return None

            # Raise error if one of the measurements is missing
            if heelMeasurement is None or hipMeasurement is None:
                raise EmptyDataException("Not enough data to calculate right hip angle")
            self.distance = distanceCalculator.calculateDistance(
                (heelMeasurement.x, heelMeasurement.y),
                (hipMeasurement.x, hipMeasurement.y),
            )
            return self.distance
        except AttributeError:
            return None

    def conditionsCheck(self, normalizedFrameMeasurement):
        angleCalculator = CalculateAnglesWithNormalizedData(normalizedFrameMeasurement)
        hipAngle = angleCalculator.calculateHipAngle()
        footAngle = -(angleCalculator.calculateFootAngle())
        kneeYCoordinate = None
        hipYCoordinate = None
        self.distance = self.calculateHeelAndHipDistance(normalizedFrameMeasurement)
        for normalizedMeasurement in normalizedFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                kneeYCoordinate = normalizedMeasurement.y
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.HIP:
                hipYCoordinate = normalizedMeasurement.y
        if (
                hipAngle is not None and
                self.distance is not None and
                footAngle is not None and
                kneeYCoordinate is not None and
                hipYCoordinate is not None
        ):
            if (
                    (10 <= hipAngle <= 60 or 80 <= hipAngle <= 150) and
                    0.07 <= abs(self.distance) <= 0.25 and
                    (10 <= abs(footAngle) <= 70) and
                    abs(kneeYCoordinate - hipYCoordinate) <= 0.2
            ):
                self.isOnRowingMachine = True
        return self.isOnRowingMachine

    def onMeasurement(self, normalizedFrameMeasurement):
        self.isOnRowingMachine = self.conditionsCheck(normalizedFrameMeasurement)
        self.notifyListeners()

    def notifyListeners(self):
        for listener in self.listeners:
            listener.onRowingMachineCheck(self.isOnRowingMachine)

    class Listener:
        def onRowingMachineCheck(self, isOnRowingMachine):
            raise NotImplementedError
