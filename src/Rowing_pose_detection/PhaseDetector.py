from src.Rowing_pose_detection.IsOnRowingMachineCheck import IsOnRowingMachineCheck
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.models.Phase import Phase
from src.pose_detection.RowingPoseDetector import RowingPoseDetector
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
        if self.currentPhase != Phase.DRIVE_PHASE and self.drivePhaseCheck():
            self.currentPhase = Phase.DRIVE_PHASE
        if self.currentPhase != Phase.RECOVERY_PHASE and self.recoveryPhaseCheck():
            self.currentPhase = Phase.RECOVERY_PHASE

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

    def extractData(self):
        if len(self.frameMeasurementBuffer) < 5:
            return False, (None, None, None, None, None, None, None, None, None, None, None, None, None)
        firstFrameMeasurement = self.frameMeasurementBuffer[-5]

        lastFrameMeasurement = self.frameMeasurementBuffer[-1]

        currentElbowAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateElbowAngle()
        previousElbowAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateElbowAngle()

        currentKneeAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()
        previousKneeAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateKneeAngle()

        currentHipAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateHipAngle()
        previousHipAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateHipAngle()

        currentShoulderAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateShoulderAngle()

        currentKneeXCoordinate = None
        currentAnkleXCoordinate = None

        currentWristXCoordinate = None
        previousWristXCoordinate = None

        currentHipXCoordinate = None
        previousHipXCoordinate = None

        for normalizedMeasurement in lastFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                currentKneeXCoordinate = normalizedMeasurement.x
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.ANKLE:
                currentAnkleXCoordinate = normalizedMeasurement.x
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                currentWristXCoordinate = normalizedMeasurement.x
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.HIP:
                currentHipXCoordinate = normalizedMeasurement.x
        for normalizedMeasurement in firstFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                previousWristXCoordinate = normalizedMeasurement.x
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.HIP:
                previousHipXCoordinate = normalizedMeasurement.x

        return True, (
            currentElbowAngle, previousElbowAngle, currentKneeAngle, previousKneeAngle, currentHipAngle,
            previousHipAngle,
            currentShoulderAngle, currentKneeXCoordinate, currentAnkleXCoordinate, currentWristXCoordinate,
            previousWristXCoordinate, currentHipXCoordinate, previousHipXCoordinate)

    def catchStateCheck(self):
        success, (
            currentElbowAngle, _, currentKneeAngle, _, currentHipAngle, _, _, currentKneeXCoordinate,
            currentAnkleXCoordinate,
            _, _, _, _) = self.extractData()
        if not success:
            return False
        if 100 < self.frameMeasurementBuffer[-1].timestamp - self.frameMeasurementBuffer[-5].timestamp < 200:
            if (currentElbowAngle is not None and 170 < currentElbowAngle <= 180) and (
                    currentKneeAngle is not None and 45 < currentKneeAngle <= 50) and (
                    currentHipAngle is not None and 20 < currentHipAngle <= 38) and (
                    currentAnkleXCoordinate is not None and currentKneeXCoordinate is not None and
                    currentAnkleXCoordinate - 0.05 <= currentKneeXCoordinate <= currentAnkleXCoordinate + 0.05):
                return True
        else:
            return False

    def drivePhaseCheck(self):
        success, (_, _, currentKneeAngle, previousKneeAngle, _, _, _, _, _, currentWristXCoordinate,
                  previousWristXCoordinate, currentHipXCoordinate, previousHipXCoordinate) = self.extractData()
        if not success:
            return False
        if 100 < self.frameMeasurementBuffer[-1].timestamp - self.frameMeasurementBuffer[-5].timestamp < 2000:
            if (
                    currentKneeAngle is not None and previousKneeAngle is not None and currentWristXCoordinate is not None and
                    previousWristXCoordinate is not None and currentHipXCoordinate is not None and previousHipXCoordinate is not None):
                if previousWristXCoordinate > currentWristXCoordinate and previousKneeAngle > currentKneeAngle or previousHipXCoordinate > currentHipXCoordinate:
                    return True
                else:
                    return False
        else:
            return False

    def finishStateCheck(self):
        success, (currentElbowAngle, _, currentKneeAngle, _, currentHipAngle, _, _, _, _, currentWristXCoordinate, _,
                  currentHipXCoordinate, _) = self.extractData()
        if not success:
            return False
        if 100 < self.frameMeasurementBuffer[-1].timestamp - self.frameMeasurementBuffer[-5].timestamp < 200:
            if (currentElbowAngle is not None and 15 <= currentElbowAngle <= 40) and (
                    currentKneeAngle is not None and 170 <= currentKneeAngle <= 180) and (
                    currentHipAngle is not None and 100 <= currentHipAngle <= 115) and (
                    currentWristXCoordinate is not None and currentHipXCoordinate is not None and
                    currentHipXCoordinate - 0.05 <= currentWristXCoordinate <= currentHipXCoordinate + 0.05):
                return True
        else:
            return False

    def recoveryPhaseCheck(self):
        success, (_, _, currentKneeAngle, previousKneeAngle, currentHipAngle, previousHipAngle, _, _, _,
                  currentWristXCoordinate, previousWristXCoordinate, _, _) = self.extractData()
        if not success:
            return False
        if 100 < self.frameMeasurementBuffer[-1].timestamp - self.frameMeasurementBuffer[-5].timestamp < 2000:
            if (currentWristXCoordinate is not None and previousWristXCoordinate is not None and
                    currentKneeAngle is not None and previousKneeAngle is not None and
                    currentHipAngle is not None and previousHipAngle is not None):
                if currentWristXCoordinate > previousWristXCoordinate and currentHipAngle < previousHipAngle:
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
