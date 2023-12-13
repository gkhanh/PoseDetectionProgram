from src.pose_detection.PoseDetector import PoseDetector
from src.models.Phase import Phase
from src.utils.CalculatedAngles import CalculatedAngles
from src.utils.Cancellable import Cancellable
from src.models.Measurement import LandmarkPosition
from src.Rowing_pose_detection.PhaseDetector import PhaseDetector


class RecoveryTechniqueAnalyzer(PhaseDetector.Listener, PoseDetector.Listener):
    def __init__(self, phaseDetector, poseDetector, frameMeasurementBuffer):
        self.frameMeasurementBuffer = frameMeasurementBuffer
        self.poseDetector = poseDetector

        # for Listeners
        self.poseDetectorCancellable = None
        self.phaseDetectorCancellable = None
        self.listeners = []

        self.feedbackMessage = None

        self.currentPhase = phaseDetector.currentPhase

    def onPhaseChange(self, currentPhase, frameMeasurementBuffer):
        if currentPhase == Phase.RECOVERY_PHASE:
            if self.poseDetectorCancellable is None:
                self.poseDetectorCancellable = self.poseDetector.addListener(self)
        else:
            if self.poseDetectorCancellable is not None:
                self.poseDetectorCancellable.cancel()

    def onMeasurement(self, frameMeasurement):
        self.frameMeasurementBuffer.append(frameMeasurement)
        self.recoveryPhaseTechniqueAnalyzer()

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

    def recoveryPhaseTechniqueAnalyzer(self):
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
            pass
            # check if the arms are straightening first by measuring the elbow angles and the shoulder angle is increasing
            # else give feedback on arms: not straightening arms
            if 150 < currentElbowAngle < 180:
                if not previousShoulderAngle < currentShoulderAngle:
                    print("Feedback: Arms are not straightening")
                    self.feedbackMessage = "Arms are not straightening"

            # make sure that the arms must move first then the body will pivot after and before the leg bends
            # by making if the arm move then check if the hip angle is decreasing or not and check if the leg angle is still around 180
            # else give feedback: need to straighten the arms first / close the body / keep the leg straight
            if previousWristXCoordinate < currentWristXCoordinate or previousElbowAngle > currentElbowAngle:
                if not previousHipAngle < currentHipAngle:
                    print("Feedback: Need to open hip")
                    self.feedbackMessage = "Need to open hip"

            # after 2 conditions above are met then check if the knee angles are decreasing and make sure the final knee angles is around 30
            # else give feedback: leg is not bent properly
            if previousKneeXCoordinate > currentKneeXCoordinate or previousKneeAngle < currentKneeAngle:
                if not 35 > previousKneeAngle > 10:
                    print("Feedback: Leg is not bent properly")
                    self.feedbackMessage = "Leg is not bent properly"

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
            listener.recoveryTechniqueAnalyzer()

    class Listener:

        def recoveryTechniqueAnalyzer(self, feedbackMessage):
            raise NotImplementedError
