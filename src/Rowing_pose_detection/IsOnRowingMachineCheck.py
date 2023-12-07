from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData
from src.pose_detection.RowingPoseDetector import RowingPoseDetector
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.models.NormalizedFrameMeasurement import NormalizedFrameMeasurement
from src.utils.Cancellable import Cancellable
from src.utils.MathUtils import MathUtils


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

    def isGrabbingHandle(self, normalizedFrameMeasurement) -> bool:
        if normalizedFrameMeasurement is None:
            return False
        wristCoordinates = None
        indexCoordinates = None
        thumbCoordinates = None
        for normalizedMeasurement in normalizedFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                wristCoordinates = normalizedMeasurement
            elif normalizedMeasurement.landmark == NormalizedLandmarkPosition.INDEX:
                indexCoordinates = normalizedMeasurement
            elif normalizedMeasurement.landmark == NormalizedLandmarkPosition.THUMB:
                thumbCoordinates = normalizedMeasurement
        if wristCoordinates and indexCoordinates and thumbCoordinates:
            angleCalculator = CalculateAnglesWithNormalizedData(normalizedFrameMeasurement)
            handAngle = angleCalculator.calculateHandAngle()
            if handAngle < 60:
                return True
        return False

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
        footAngle = 180 + angleCalculator.calculateFootAngle()
        self.distance = self.calculateHeelAndHipDistance(normalizedFrameMeasurement)
        if not self.isGrabbingHandle(normalizedFrameMeasurement):
            self.isOnRowingMachine = False
        if (
                hipAngle is not None and
                self.distance is not None and
                footAngle is not None
        ):
            if (
                    (10 <= hipAngle <= 60 or 80 <= hipAngle <= 140) and
                    0.07 <= abs(self.distance) <= 0.25 and
                    (10 <= abs(footAngle) <= 90)
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
