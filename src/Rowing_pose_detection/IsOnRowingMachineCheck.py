<<<<<<< HEAD
from src.models.measurement import LandmarkPosition
from src.pose_detection.PoseDetector import PoseDetector
from src.utils.CalculatedAngles import CalculatedAngles
from src.utils.Cancellable import Cancellable
from src.utils.MathUtils import MathUtils


class IsOnRowingMachineCheck(PoseDetector.Listener):
    def __init__(self, poseDetector) -> None:
        self.poseDetector = poseDetector
=======
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
>>>>>>> master
        self.distance = 0.0
        self.listeners = []
        self.isOnRowingMachine = False
        self.poseDetectorCancellable = None

    def addListener(self, listener):
        self.listeners.append(listener)
        listener.onRowingMachineCheck(self.isOnRowingMachine)

        if len(self.listeners) == 1:
<<<<<<< HEAD
            self.poseDetectorCancellable = self.poseDetector.addListener(self)
=======
            self.poseDetectorCancellable = self.rowingPoseDetector.addListener(self)
>>>>>>> master

        return Cancellable(lambda: self._removeListener(listener))

    def _removeListener(self, listener):
        self.listeners.remove(listener)
        if len(self.listeners) == 0:
            self.poseDetectorCancellable.cancel()

<<<<<<< HEAD
    def isGrabbingHandle(self, frameMeasurement) -> bool:
        if frameMeasurement is None:
            return False

        rightWristCoordinates = None
        rightIndexCoordinates = None
        rightThumbCoordinates = None
        leftWristCoordinates = None
        leftIndexCoordinates = None
        leftThumbCoordinates = None

        for measurement in frameMeasurement.measurements:
            if measurement.landmark == LandmarkPosition.RIGHT_WRIST:
                rightWristCoordinates = measurement
            elif measurement.landmark == LandmarkPosition.RIGHT_INDEX:
                rightIndexCoordinates = measurement
            elif measurement.landmark == LandmarkPosition.RIGHT_THUMB:
                rightThumbCoordinates = measurement
            elif measurement.landmark == LandmarkPosition.LEFT_WRIST:
                leftWristCoordinates = measurement
            elif measurement.landmark == LandmarkPosition.LEFT_INDEX:
                leftIndexCoordinates = measurement
            elif measurement.landmark == LandmarkPosition.LEFT_THUMB:
                leftThumbCoordinates = measurement

        if (rightWristCoordinates and rightIndexCoordinates and rightThumbCoordinates) or \
                (leftWristCoordinates and leftIndexCoordinates and leftThumbCoordinates):
            angleCalculator = CalculatedAngles(frameMeasurement)
            leftHandAngle = angleCalculator.calculateLeftHandAngle()
            rightHandAngle = angleCalculator.calculateRightHandAngle()

            if leftHandAngle < 30 or rightHandAngle < 30:
                return True

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
=======
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
>>>>>>> master
            )
            return self.distance
        except AttributeError:
            return None

<<<<<<< HEAD
    def conditionsCheck(self, frameMeasurement):
        angleCalculator = CalculatedAngles(frameMeasurement)
        rightHipAngle = angleCalculator.calculateRightHipAngle()
        leftHipAngle = angleCalculator.calculateLeftHipAngle()
        leftFootAngle = angleCalculator.calculateLeftFootAngle()
        rightFootAngle = angleCalculator.calculateRightFootAngle()
        self.distance = self.calculateHeelAndHipDistance(frameMeasurement)
        if not self.isGrabbingHandle(frameMeasurement):
            self.isOnRowingMachine = False
        if (
                rightHipAngle is not None and
                leftHipAngle is not None and
                self.distance is not None and
                leftFootAngle is not None and
                rightFootAngle is not None
        ):
            if (
                    (10 <= rightHipAngle <= 60 or 60 <= leftHipAngle <= 130) and
                    0.074 <= abs(self.distance) <= 0.19 and
                    (18 <= abs(leftFootAngle) <= 77 or 18 <= abs(rightFootAngle) <= 77)
=======
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
>>>>>>> master
            ):
                self.isOnRowingMachine = True
        return self.isOnRowingMachine

<<<<<<< HEAD
    def onMeasurement(self, frameMeasurement):
        self.isOnRowingMachine = self.conditionsCheck(frameMeasurement)
=======
    def onMeasurement(self, normalizedFrameMeasurement):
        self.isOnRowingMachine = self.conditionsCheck(normalizedFrameMeasurement)
>>>>>>> master
        self.notifyListeners()

    def notifyListeners(self):
        for listener in self.listeners:
            listener.onRowingMachineCheck(self.isOnRowingMachine)

    class Listener:
        def onRowingMachineCheck(self, isOnRowingMachine):
            raise NotImplementedError
