from src.models.Phase import Phase
from src.pose_detection.RowingPoseDetector import RowingPoseDetector
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData
from src.utils.Cancellable import Cancellable
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.Rowing_pose_detection.PhaseDetector import PhaseDetector


class DriveTechniqueAnalyzer(PhaseDetector.Listener, RowingPoseDetector.Listener):
    def __init__(self, phaseDetector, rowingPoseDetector, frameMeasurementBuffer):
        self.frameMeasurementBuffer = frameMeasurementBuffer
        self.rowingPoseDetector = rowingPoseDetector

        # for Listeners
        self.poseDetectorCancellable = None
        self.phaseDetectorCancellable = None
        self.listeners = []

        self.feedbackMessage = None

        self.currentPhase = phaseDetector.currentPhase

    def onPhaseChange(self, currentPhase, frameMeasurementBuffer):
        if currentPhase == Phase.DRIVE_PHASE:
            if self.poseDetectorCancellable is None:
                self.poseDetectorCancellable = self.poseDetector.addListener(self)
        else:
            if self.poseDetectorCancellable is not None:
                self.poseDetectorCancellable.cancel()

    def onMeasurement(self, normalizedFrameMeasurement):
        self.frameMeasurementBuffer.append(normalizedFrameMeasurement)
        self.drivePhaseTechniqueAnalyzer()

    def collectingData(self):
        firstFrameMeasurement = self.frameMeasurementBuffer[-5]
        lastFrameMeasurement = self.frameMeasurementBuffer[-1]

        hipAngle1 = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateHipAngle()
        hipAngle2 = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateHipAngle()
        elbowAngle1 = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateElbowAngle()
        elbowAngle2 = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateElbowAngle()
        kneeAngle1 = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateKneeAngle()
        kneeAngle2 = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()
        shoulderAngle1 = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateShoulderAngle()
        shoulderAngle2 = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateShoulderAngle()

        wristXCoordinate1 = None
        wristXCoordinate2 = None
        kneeXCoordinate1 = None
        kneeXCoordinate2 = None

        for normalizedMeasurement in firstFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                wristXCoordinate1 = normalizedMeasurement.x
            elif normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                kneeXCoordinate1 = normalizedMeasurement.x
        for normalizedMeasurement in lastFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                wristXCoordinate2 = normalizedMeasurement.x
            elif normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                kneeXCoordinate2 = normalizedMeasurement.x

        dataCollection = [hipAngle1, hipAngle2, elbowAngle1, elbowAngle2, kneeAngle1, kneeAngle2, shoulderAngle1,
                          shoulderAngle2, wristXCoordinate1, wristXCoordinate2, kneeXCoordinate1, kneeXCoordinate2]
        return dataCollection

    def drivePhaseTechniqueAnalyzer(self):
        dataCollection = self.collectingData()
        previousHipAngle = dataCollection[0]
        currentHipAngle = dataCollection[1]
        previousElbowAngle = dataCollection[2]
        currentElbowAngle = dataCollection[3]
        previousKneeAngle = dataCollection[4]
        currentKneeAngle = dataCollection[5]
        previousShoulderAngle = dataCollection[6]
        currentShoulderAngle = dataCollection[7]
        previousWristXCoordinate = dataCollection[8]
        currentWristXCoordinate = dataCollection[9]
        previousKneeXCoordinate = dataCollection[10]
        currentKneeXCoordinate = dataCollection[11]
        if dataCollection is not None:
            # measure the knee angles, check if the knees angles is less than 100 degree, then the hip angles has to be stayed less than 90 degree
            # else give feedback on hip: open hip too soon
            if currentKneeAngle < 100:
                if currentHipAngle >= 90:
                    print("Feedback: Open hip too soon")
                    self.feedbackMessage = "Open hip too soon"

            # measure the hip angles, check if the knees angles is more than 100 degree, then check if the hip angles is increasing or not
            # else give feedback on hip opening: not opening hip
            elif previousKneeAngle > 100:
                if previousHipAngle <= 90 and previousHipAngle - 5 < currentHipAngle < previousHipAngle + 5:
                    print("Feedback: Hip is not open")
                    self.feedbackMessage = "Hip is not open"

            # check if the knee angles is around 180 degree (fully extended) and hip angles is more than 100 degree
            # else give feedback on hip opening: not opening hip, leg not fully extended
            if currentKneeAngle < 140:
                print("Feedback: Leg not fully extended")
                self.feedbackMessage = "Leg not fully extended"
            else:
                if currentHipAngle < 100 and previousHipAngle - 5 < currentHipAngle < previousHipAngle + 5:
                    print("Feedback: Hip is not open")
                    self.feedbackMessage = "Hip is not open"

            # check when the user can pull back the arm by comparing the x coordinates of both wrists and knees, if they are equal
            # else give feedback: pull arm too soon/early
            # check if the previous condition is met, then check the x coordinates of both wrists if its decreasing(?) and shoulder angle is decreasing
            # else give feedback: arm not pulled back
            if currentKneeXCoordinate - 0.05 <= currentWristXCoordinate <= currentKneeXCoordinate + 0.05:
                if not previousWristXCoordinate < currentWristXCoordinate:
                    print("Feedback: Not pulling arm")
                    self.feedbackMessage = "Not pulling arm"

            # check if the arms are fully pulled back by checking the shoulder angla is less than 10 degree and elbow angles is around 90 degree
            # else give feedback: arm not pulled back properly
            if not currentShoulderAngle < 10 and 60 < currentElbowAngle <= 95:
                print("Feedback: Arm not pulled back properly")
                self.feedbackMessage = "Arm not pulled back properly"

    def addListener(self, listener):
        self.listeners.append(listener)
        if len(self.listeners) == 1:
            self.phaseDetectorCancellable = self.phaseDetector.addListener(self)
        return Cancellable(lambda: self._removeListener(listener))

    def _removeListener(self, listener):
        self.listeners.remove(listener)
        if len(self.listeners) == 0 and self.phaseDetectorCancellable is not None:
            self.phaseDetectorCancellable.cancel()

    def notifyListeners(self):
        for listener in self.listeners:
            listener.driveTechniqueAnalyzer()

    class Listener:

        def driveTechniqueAnalyzer(self, feedbackMessage):
            raise NotImplementedError
