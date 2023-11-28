from src.models.FrameMeasurement import FrameMeasurement
from src.models.measurement import Measurement, LandmarkPosition
from src.utils.CalculatedAngles import CalculatedAngles
from src.Rowing_pose_detection.IsOnRowingMachineCheck import IsOnRowingMachineCheck


class DrivePhasePrerequisite:
    def __init__(self, isOnRowingMachineCheck, poseDetector):
        self.bodyAngles = []
        isOnRowingMachineCheck.addListener(self.isOnRowingMachineCheck)
        poseDetector.addListener(self.onMeasurement)
        self.onRowingMachine = False
        self.previousTimestamp = 0
        self.result = False
        self.listeners = []
        pass

    def addListener(self, listener):
        self.listeners.append(listener)
        return Cancellable(lambda: self.listeners.remove(listener))

    def onMeasurement(self, frameMeasurement):
        if self.isOnRowingMachine:
            self.drivePhaseCheck(frameMeasurement)

    def isOnRowingMachine(self, isOnRowingMachine):
        self.onRowingMachine = isOnRowingMachine
        return self.onRowingMachine

    def Drive(self, frameMeasurement):
        self.notifyListeners()
        if self.isOnRowingMachine() and self.drivePhaseCheck(frameMeasurement):
            print('On drive phase')
            self.result = True
        else:
            print('Not on drive phase')
        return self.result

    def drivePhaseCheck(self, frameMeasurement):
        angleCalculator = CalculatedAngles(frameMeasurement)
        leftKneeAngle = angleCalculator.calculateLeftKneeAngle()
        rightKneeAngle = angleCalculator.calculateRightKneeAngle()

        if leftKneeAngle < 80 or rightKneeAngle < 80 and 200 <= frameMeasurement.timestamp - self.previousTimestamp <= 2000:
            print('On drive phase')
            return True
        self.previousTimestamp = frameMeasurement.timestamp

        return False

    def notifyListeners(self):
        for listener in self.listeners:
            listener.onRowingMachineCheck(self)

    class Listener:
        def onRowingMachineCheck(self):
            raise NotImplementedError
