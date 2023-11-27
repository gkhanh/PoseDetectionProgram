from src.utils.CalculatedAngles import CalculatedAngles
from src.models.measurement import LandmarkPosition
from src.utils.Cancellable import Cancellable


class IsOnRowingMachineCheck:
    def __init__(self) -> None:
        self.bodyAngles = []
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
            print("Grabbing handle")
            leftHandAngle = CalculatedAngles.calculateLeftHandAngle(frameMeasurement)
            rightHandAngle = CalculatedAngles.calculateRightHandAngle(frameMeasurement)
            print(f'leftHandAngle: {leftHandAngle}, rightHandAngle: {rightHandAngle}')
            return True
        else:
            leftHandAngle = CalculatedAngles.calculateLeftHandAngle(frameMeasurement)
            rightHandAngle = CalculatedAngles.calculateRightHandAngle(frameMeasurement)
            print(f'leftHandAngle: {leftHandAngle}, rightHandAngle: {rightHandAngle}')
            print("Not grabbing handle")
            return False

    def onRowingMachineCheck(self, frameMeasurement) -> bool:
        if not self.isGrabbingHandle(frameMeasurement):
            self.result = False
        rightHipAngle = CalculatedAngles.calculateRightHipAngle(frameMeasurement)
        rightKneeAngle = CalculatedAngles.calculateRightKneeAngle(frameMeasurement)
        leftHipAngle = CalculatedAngles.calculateLeftHipAngle(frameMeasurement)
        leftKneeAngle = CalculatedAngles.calculateLeftKneeAngle(frameMeasurement)
        if (60 <= rightHipAngle <= 90 or 100 <= rightHipAngle <= 120) or (60 <= leftHipAngle <= 90 or 100 <= leftHipAngle <= 120):
            self.result = True
        self.notifyListeners()
        return self.result

    def notifyListeners(self):
        for listener in self.listeners:
            listener.onRowingMachineCheck(self)

    class Listener:
        def onRowingMachineCheck(self):
            raise NotImplementedError
