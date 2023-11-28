from src.models.measurement import LandmarkPosition
from src.utils.CalculatedAngles import CalculatedAngles
from src.utils.Cancellable import Cancellable
from src.utils.MathUtils import MathUtils


class IsOnRowingMachineCheck:
    def __init__(self) -> None:
        self.distance = 0.0
        self.listeners = []
        self.result = False

    def addListener(self, listener):
        self.listeners.append(listener)

        return Cancellable(lambda: self.listeners.remove(listener))

    def isGrabbingHandle(self, frameMeasurement) -> bool:
        rightWristCoordinates = None
        rightIndexCoordinates = None
        rightThumbCoordinates = None
        leftWristCoordinates = None
        leftIndexCoordinates = None
        leftThumbCoordinates = None
        leftHandAngle = 0
        rightHandAngle = 0
        if frameMeasurement is None:
            return False
        for measurement in frameMeasurement.measurements:
            if measurement.landmark == LandmarkPosition.RIGHT_WRIST:
                rightWristCoordinates = measurement
            if measurement.landmark == LandmarkPosition.RIGHT_INDEX:
                rightIndexCoordinates = measurement
            if measurement.landmark == LandmarkPosition.RIGHT_THUMB:
                rightThumbCoordinates = measurement
            if measurement.landmark == LandmarkPosition.LEFT_WRIST:
                leftWristCoordinates = measurement
            if measurement.landmark == LandmarkPosition.LEFT_INDEX:
                leftIndexCoordinates = measurement
            if measurement.landmark == LandmarkPosition.LEFT_THUMB:
                leftThumbCoordinates = measurement
        if (
                rightWristCoordinates is not None
                and rightIndexCoordinates is not None
                and rightThumbCoordinates is not None
                or leftWristCoordinates is not None
                and leftIndexCoordinates is not None
                and leftThumbCoordinates is not None
        ):
            angleCalculator = CalculatedAngles(frameMeasurement)
            leftHandAngle = angleCalculator.calculateLeftHandAngle()
            rightHandAngle = angleCalculator.calculateRightHandAngle()
        if leftHandAngle < 30 or rightHandAngle < 30:
            return True
        else:
            return False

    def calculateHeelAndHipDistance(self, frameMeasurement):
        try:
            distanceCalculator = MathUtils()
            # Find the RIGHT_HEEL
            rightHeelMeasurement = None
            if not frameMeasurement.measurements:
                return None
            for measurement in frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.RIGHT_HEEL:
                    rightHeelMeasurement = measurement
                    break
            if rightHeelMeasurement is None:
                return None

            # Find the RIGHT_HIP
            rightHipMeasurement = None
            if not frameMeasurement.measurements:
                return None
            for measurement in frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.RIGHT_HIP:
                    rightHipMeasurement = measurement
                    break
            if rightHipMeasurement is None:
                return None

            # Raise error if one of the measurements is missing
            if rightHeelMeasurement is None or rightHipMeasurement is None:
                raise EmptyDataException("Not enough data to calculate right hip angle")
            self.distance = distanceCalculator.calculateDistance(
                (rightHeelMeasurement.x, rightHeelMeasurement.y),
                (rightHipMeasurement.x, rightHipMeasurement.y),
            )
            return self.distance
        except AttributeError:
            return None

    def conditionsCheck(self, frameMeasurement):
        angleCalculator = CalculatedAngles(frameMeasurement)
        rightHipAngle = angleCalculator.calculateRightHipAngle()
        leftHipAngle = angleCalculator.calculateLeftHipAngle()
        leftFootAngle = angleCalculator.calculateLeftFootAngle()
        rightFootAngle = angleCalculator.calculateRightFootAngle()
        self.distance = self.calculateHeelAndHipDistance(frameMeasurement)
        if not self.isGrabbingHandle(frameMeasurement):
            self.result = False
        else:
            if (rightHipAngle is not None and leftHipAngle is not None and self.distance is not None
                    and leftFootAngle is not None and rightFootAngle is not None):
                if (10 <= rightHipAngle <= 60 or 60 <= leftHipAngle <= 130) and 0.074 <= abs(
                        self.distance) <= 0.19 and (18 <= abs(leftFootAngle) <= 77 or 18 <= abs(rightFootAngle) <= 77):
                    self.result = True
                else:
                    self.result = False
        return self.result

    def onRowingMachineCheck(self, frameMeasurement):
        self.result = self.conditionsCheck(frameMeasurement)
        self.notifyListeners()

    def notifyListeners(self):
        for listener in self.listeners:
            listener.onRowingMachineCheck(self.result)

    class Listener:
        def onRowingMachineCheck(self):
            raise NotImplementedError
