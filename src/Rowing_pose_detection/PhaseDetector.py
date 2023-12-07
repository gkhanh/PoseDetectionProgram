from src.Rowing_pose_detection.IsOnRowingMachineCheck import IsOnRowingMachineCheck
from src.pose_detection.RowingPoseDetector import RowingPoseDetector
from src.models.NormalizedFrameMeasurement import NormalizedFrameMeasurement
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.models.Phase import Phase
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData
from src.utils.Cancellable import Cancellable


class PhaseDetector(IsOnRowingMachineCheck.Listener, RowingPoseDetector.Listener):
    def __init__(self, isOnRowingMachineCheck, rowingPoseDetector):
        # For listener
        self.isOnRowingMachineCheck = isOnRowingMachineCheck
        self.rowingPoseDetector = rowingPoseDetector
        self.isOnRowingMachineCheckCancellable = None
        self.poseDetectorCancellable = None
        self.listeners = []

        # For storing frame measurements
        self.frameMeasurementBuffer = []

        self.currentPhase = Phase.OTHER

    def onRowingMachineCheck(self, isOnRowingMachine):
        if isOnRowingMachine:
            if self.poseDetectorCancellable is None:
                self.poseDetectorCancellable = self.rowingPoseDetector.addListener(self)
        else:
            if self.poseDetectorCancellable is not None:
                self.poseDetectorCancellable.cancel()
                self.poseDetectorCancellable = None

    def onMeasurement(self, normalizedFrameMeasurement):
        currentPhase = self.currentPhase
        self.collectFrameMeasurement(normalizedFrameMeasurement)

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

    def collectFrameMeasurement(self, normalizedFrameMeasurement):
        self.frameMeasurementBuffer.append(normalizedFrameMeasurement)

    def drivePhaseCheck(self):
        if len(self.frameMeasurementBuffer) < 5:
            return False
        firstFrameMeasurement = self.frameMeasurementBuffer[-5]
        lastFrameMeasurement = self.frameMeasurementBuffer[-1]
        kneeAngle1 = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateKneeAngle()
        kneeAngle2 = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()
        wristXCoordinate1 = None
        wristXCoordinate2 = None
        for normalizedMeasurement in firstFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                wristXCoordinate1 = normalizedMeasurement.x
        for normalizedMeasurement in lastFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                wristXCoordinate2 = normalizedMeasurement.x
        if 100 < lastFrameMeasurement.timestamp - firstFrameMeasurement.timestamp < 2000:
            if (kneeAngle1 is not None and kneeAngle2 is not None and wristXCoordinate1 is not None and
                    wristXCoordinate2 is not None):
                if kneeAngle1 < kneeAngle2 and wristXCoordinate1 > wristXCoordinate2:
                    return True
        else:
            return False

    def recoveryPhaseCheck(self):
        if len(self.frameMeasurementBuffer) < 5:
            return False
        firstFrameMeasurement = self.frameMeasurementBuffer[-5]
        lastFrameMeasurement = self.frameMeasurementBuffer[-1]
        kneeAngle1 = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateKneeAngle()
        kneeAngle2 = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()
        wristXCoordinate1 = None
        wristXCoordinate2 = None
        for normalizedMeasurement in firstFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                wristXCoordinate1 = normalizedMeasurement.x
        for normalizedMeasurement in lastFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                wristXCoordinate2 = normalizedMeasurement.x
        if 100 < lastFrameMeasurement.timestamp - firstFrameMeasurement.timestamp < 2000:
            if (kneeAngle1 is not None and kneeAngle2 is not None and wristXCoordinate1 is not None and
                    wristXCoordinate2 is not None):
                if kneeAngle1 > kneeAngle2 and wristXCoordinate1 < wristXCoordinate2:
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
            self.isOnRowingMachineCheckCancellable = None

    def notifyListeners(self, frameMeasurementBuffer):
        for listener in self.listeners:
            listener.onPhaseChange(self.currentPhase, frameMeasurementBuffer)

    class Listener:

        def onPhaseChange(self, currentPhase, frameMeasurementBuffer):
            raise NotImplementedError
