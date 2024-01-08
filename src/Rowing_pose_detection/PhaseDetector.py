from src.Rowing_pose_detection.IsOnRowingMachineCheck import IsOnRowingMachineCheck
<<<<<<< HEAD
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
=======
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
>>>>>>> master

        # For storing frame measurements
        self.frameMeasurementBuffer = []

<<<<<<< HEAD
        self.onRowingMachine = False
        self.previousTimestamp = 0.0
        self.currentPhase = Phase.OTHER
        self.listeners = []
=======
        self.currentPhase = Phase.OTHER
>>>>>>> master

    def onRowingMachineCheck(self, isOnRowingMachine):
        if isOnRowingMachine:
            if self.poseDetectorCancellable is None:
<<<<<<< HEAD
                self.poseDetectorCancellable = self.poseDetector.addListener(self)
=======
                self.poseDetectorCancellable = self.rowingPoseDetector.addListener(self)
>>>>>>> master
        else:
            if self.poseDetectorCancellable is not None:
                self.poseDetectorCancellable.cancel()
                self.poseDetectorCancellable = None

<<<<<<< HEAD
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
=======
    def onMeasurement(self, normalizedFrameMeasurement):
        currentPhase = self.currentPhase
        self.collectFrameMeasurement(normalizedFrameMeasurement)
        if self.currentPhase != Phase.DRIVE_PHASE and self.drivePhaseCheck():
            self.currentPhase = Phase.DRIVE_PHASE
        if self.currentPhase != Phase.RECOVERY_PHASE and self.recoveryPhaseCheck():
            self.currentPhase = Phase.RECOVERY_PHASE
>>>>>>> master

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

<<<<<<< HEAD
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
=======
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
>>>>>>> master
        else:
            return False

    def recoveryPhaseCheck(self):
<<<<<<< HEAD
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
=======
        success, (_, _, currentKneeAngle, previousKneeAngle, currentHipAngle, previousHipAngle, _, _, _,
                  currentWristXCoordinate, previousWristXCoordinate, _, _) = self.extractData()
        if not success:
            return False
        if 100 < self.frameMeasurementBuffer[-1].timestamp - self.frameMeasurementBuffer[-5].timestamp < 2000:
            if (currentWristXCoordinate is not None and previousWristXCoordinate is not None and
                    currentKneeAngle is not None and previousKneeAngle is not None and
                    currentHipAngle is not None and previousHipAngle is not None):
                if currentWristXCoordinate > previousWristXCoordinate and currentHipAngle < previousHipAngle:
>>>>>>> master
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
<<<<<<< HEAD
=======
            self.isOnRowingMachineCheckCancellable = None
>>>>>>> master

    def notifyListeners(self, frameMeasurementBuffer):
        for listener in self.listeners:
            listener.onPhaseChange(self.currentPhase, frameMeasurementBuffer)

    class Listener:

<<<<<<< HEAD
        def onPhaseChange(self, phase, frameMeasurementBuffer):
=======
        def onPhaseChange(self, currentPhase, frameMeasurementBuffer):
>>>>>>> master
            raise NotImplementedError
