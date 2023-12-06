from src.Rowing_pose_detection.IsOnRowingMachineCheck import IsOnRowingMachineCheck
from src.models.Phase import Phase
from src.pose_detection.PoseDetector import PoseDetector
from src.utils.CalculatedAngles import CalculatedAngles
from src.utils.Cancellable import Cancellable
from src.models.measurement import LandmarkPosition


class PhaseDetector(IsOnRowingMachineCheck.Listener, PoseDetector.Listener):
    def __init__(self, isOnRowingMachineCheck, poseDetector):
        # For listener
        self.isOnRowingMachineCheck = isOnRowingMachineCheck
        self.poseDetector = poseDetector
        self.isOnRowingMachineCheckCancellable = None
        self.poseDetectorCancellable = None
        self.listeners = []

        # For storing frame measurements
        self.frameMeasurementBuffer = []

        self.currentPhase = Phase.OTHER

    def onRowingMachineCheck(self, isOnRowingMachine):
        if isOnRowingMachine:
            if self.poseDetectorCancellable is None:
                self.poseDetectorCancellable = self.poseDetector.addListener(self)
        else:
            if self.poseDetectorCancellable is not None:
                self.poseDetectorCancellable.cancel()
                self.poseDetectorCancellable = None

    def onMeasurement(self, frameMeasurement):
        currentPhase = self.currentPhase
        self.collectFrameMeasurement(frameMeasurement)

        if self.drivePhaseCheck():
            print('On drive phase')
            self.currentPhase = Phase.DRIVE_PHASE
        elif self.recoveryPhaseCheck():
            print('On recovery phase')
            self.currentPhase = Phase.RECOVERY_PHASE
        else:
            self.currentPhase = Phase.OTHER

        if currentPhase != self.currentPhase:
            if self.currentPhase == Phase.DRIVE_PHASE:
                print('Started a new drive')
            elif self.currentPhase == Phase.RECOVERY_PHASE:
                print('Started a new recovery')
            else:
                print('Ended a drive or recovery')

            self.notifyListeners(self.frameMeasurementBuffer)
            # Reset frame measurement buffer but include the last five datapoints
            self.frameMeasurementBuffer = self.frameMeasurementBuffer[-5:]

    def collectFrameMeasurement(self, frameMeasurement):
        self.frameMeasurementBuffer.append(frameMeasurement)

    def drivePhaseCheck(self):
        if len(self.frameMeasurementBuffer) < 5:
            return False
        firstFrameMeasurement = self.frameMeasurementBuffer[-5]
        lastFrameMeasurement = self.frameMeasurementBuffer[-1]
        leftKneeAngle1 = CalculatedAngles(firstFrameMeasurement).calculateLeftKneeAngle()
        leftKneeAngle2 = CalculatedAngles(lastFrameMeasurement).calculateLeftKneeAngle()
        rightKneeAngle1 = CalculatedAngles(firstFrameMeasurement).calculateRightKneeAngle()
        rightKneeAngle2 = CalculatedAngles(lastFrameMeasurement).calculateRightKneeAngle()
        leftWristXCoordinate1 = None
        rightWristXCoordinate1 = None
        leftWristXCoordinate2 = None
        rightWristXCoordinate2 = None
        for measurement in firstFrameMeasurement.measurements:
            if measurement.landmark == LandmarkPosition.LEFT_WRIST:
                leftWristXCoordinate1 = measurement.x
            elif measurement.landmark == LandmarkPosition.RIGHT_WRIST:
                rightWristXCoordinate1 = measurement.x
        for measurement in lastFrameMeasurement.measurements:
            if measurement.landmark == LandmarkPosition.LEFT_WRIST:
                leftWristXCoordinate2 = measurement.x
            elif measurement.landmark == LandmarkPosition.RIGHT_WRIST:
                rightWristXCoordinate2 = measurement.x

        print(f'interval: {lastFrameMeasurement.timestamp - firstFrameMeasurement.timestamp}')
        if 100 < lastFrameMeasurement.timestamp - firstFrameMeasurement.timestamp < 2000:
            if (leftKneeAngle1 is not None and leftKneeAngle2 is not None and rightKneeAngle1 is not None and
                    rightKneeAngle2 is not None and leftWristXCoordinate1 is not None and
                    leftWristXCoordinate2 is not None and rightWristXCoordinate1 is not None and
                    rightWristXCoordinate2 is not None):
                if ((leftKneeAngle1 < leftKneeAngle2 or rightKneeAngle1 < rightKneeAngle2) and
                        (leftWristXCoordinate1 > leftWristXCoordinate2 or rightWristXCoordinate1 > rightWristXCoordinate2)):
                    return True
        else:
            return False

    def recoveryPhaseCheck(self):
        if len(self.frameMeasurementBuffer) < 5:
            return False
        firstFrameMeasurement = self.frameMeasurementBuffer[-5]
        lastFrameMeasurement = self.frameMeasurementBuffer[-1]
        leftKneeAngle1 = CalculatedAngles(firstFrameMeasurement).calculateLeftKneeAngle()
        leftKneeAngle2 = CalculatedAngles(lastFrameMeasurement).calculateLeftKneeAngle()
        rightKneeAngle1 = CalculatedAngles(firstFrameMeasurement).calculateRightKneeAngle()
        rightKneeAngle2 = CalculatedAngles(lastFrameMeasurement).calculateRightKneeAngle()
        leftWristXCoordinate1 = None
        rightWristXCoordinate1 = None
        leftWristXCoordinate2 = None
        rightWristXCoordinate2 = None
        for measurement in firstFrameMeasurement.measurements:
            if measurement.landmark == LandmarkPosition.LEFT_WRIST:
                leftWristXCoordinate1 = measurement.x
            elif measurement.landmark == LandmarkPosition.RIGHT_WRIST:
                rightWristXCoordinate1 = measurement.x
        for measurement in lastFrameMeasurement.measurements:
            if measurement.landmark == LandmarkPosition.LEFT_WRIST:
                leftWristXCoordinate2 = measurement.x
            elif measurement.landmark == LandmarkPosition.RIGHT_WRIST:
                rightWristXCoordinate2 = measurement.x
        print(f'interval: {lastFrameMeasurement.timestamp - firstFrameMeasurement.timestamp}')
        if 100 < lastFrameMeasurement.timestamp - firstFrameMeasurement.timestamp < 2000:
            if (leftKneeAngle1 is not None and leftKneeAngle2 is not None and rightKneeAngle1 is not None and
                    rightKneeAngle2 is not None and leftWristXCoordinate1 is not None and
                    leftWristXCoordinate2 is not None and rightWristXCoordinate1 is not None and
                    rightWristXCoordinate2 is not None):
                if ((leftKneeAngle1 > leftKneeAngle2 or rightKneeAngle1 > rightKneeAngle2) and
                        (leftWristXCoordinate1 < leftWristXCoordinate2 or rightWristXCoordinate1 < rightWristXCoordinate2)):
                    return True
        else:
            return False

    def addListener(self, listener):
        self.listeners.append(listener)
        if len(self.listeners) == 1:
            self.isOnRowingMachineCheckCancellable = self.isOnRowingMachineCheck.addListener(self)
        return Cancellable(lambda: self._removeListener(listener))

    def _removeListener(self, listener):
        self.listeners.remove(listener)
        if len(self.listeners) == 0 and self.isOnRowingMachineCheckCancellable is not None:
            self.isOnRowingMachineCheckCancellable.cancel()

    def notifyListeners(self, frameMeasurementBuffer):
        for listener in self.listeners:
            listener.onPhaseChange(self.currentPhase, frameMeasurementBuffer)

    class Listener:

        def onPhaseChange(self, currentPhase, frameMeasurementBuffer):
            raise NotImplementedError
