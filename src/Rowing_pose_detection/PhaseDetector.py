from src.Rowing_pose_detection.IsOnRowingMachineCheck import IsOnRowingMachineCheck
from src.models.Phase import Phase
from src.pose_detection.PoseDetector import PoseDetector
from src.utils.CalculatedAngles import CalculatedAngles
from src.utils.Cancellable import Cancellable


class DrivePhaseDetector(IsOnRowingMachineCheck.Listener, PoseDetector.Listener):
    def __init__(self, isOnRowingMachineCheck, poseDetector):
        self.isOnRowingMachineCheck = isOnRowingMachineCheck
        self.poseDetector = poseDetector

        self.isOnRowingMachineCheckCancellable = None
        self.poseDetectorCancellable = None

        self.lastFiveFrameMeasurements = []
        self.bodyAngles = []
        self.onRowingMachine = False
        self.previousLeftKneeAngle = None
        self.previousRightKneeAngle = None
        self.previousTimestamp = 0.0
        self.result = False
        self.listeners = []

    def addListener(self, listener):
        self.listeners.append(listener)
        if len(self.listeners) == 1:
            self.isOnRowingMachineCheckCancellable = self.isOnRowingMachineCheck.addListener(self)
        return Cancellable(lambda: self._removeListener(listener))

    def _removeListener(self, listener):
        self.listeners.remove(listener)
        if len(self.listeners) == 0 and self.isOnRowingMachineCheckCancellable is not None:
            self.isOnRowingMachineCheckCancellable.cancel()

    def onRowingMachineCheck(self, isOnRowingMachine):
        if isOnRowingMachine:
            self.poseDetectorCancellable = self.poseDetector.addListener(self)
        else:
            if self.poseDetectorCancellable is not None:
                self.poseDetectorCancellable.cancel()

    def onMeasurement(self, frameMeasurement):
        previousResult = self.result
        if self.isOnRowingMachineCheck:
            if self.drivePhaseCheck(frameMeasurement):
                print('On drive phase')
                self.result = True
            else:
                print('Not on drive phase')
                self.result = False
        if previousResult != self.result:
            self.notifyListeners()

    def drivePhaseCheck(self, frameMeasurement):
        self.lastFiveFrameMeasurements.append(frameMeasurement)
        if len(self.lastFiveFrameMeasurements) > 5:
            self.lastFiveFrameMeasurements.pop(0)

        firstFrameMeasurement = self.lastFiveFrameMeasurements[0]
        if firstFrameMeasurement is None:
            return False

        lastFrameMeasurement = self.lastFiveFrameMeasurements[-1]
        if lastFrameMeasurement is None:
            return False

        angleCalculator = CalculatedAngles(frameMeasurement)
        leftKneeAngle = angleCalculator.calculateLeftKneeAngle()
        rightKneeAngle = angleCalculator.calculateRightKneeAngle()

        if (leftKneeAngle is not None and leftKneeAngle < 160) or (
                rightKneeAngle is not None and rightKneeAngle < 160) and 200 <= frameMeasurement.timestamp - self.previousTimestamp <= 2000:
            return True
        self.previousTimestamp = frameMeasurement.timestamp
        return False

    def notifyListeners(self):
        for listener in self.listeners:
            if self.result:
                listener.onPhaseChange(Phase.DRIVE_PHASE)
            else:
                listener.onPhaseChange(Phase.RECOVERY_PHASE)

    class Listener:

        def onPhaseChange(self, Phase):
            # raise NotImplementedError
            pass

