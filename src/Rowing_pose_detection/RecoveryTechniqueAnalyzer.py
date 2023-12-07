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

    def recoveryPhaseTechniqueAnalyzer(self, frameMeasurementBuffer):
        for frameMeasurement in frameMeasurementBuffer:
            leftHipAngle = CalculatedAngles(frameMeasurement).calculateLeftHipAngle()
            rightHipAngle = CalculatedAngles(frameMeasurement).calculateRightHipAngle()
            leftElbowAngle = CalculatedAngles(frameMeasurement).calculateLeftElbowAngle()
            rightElbowAngle = CalculatedAngles(frameMeasurement).calculateRightElbowAngle()
            leftKneeAngle = CalculatedAngles(frameMeasurement).calculateLeftKneeAngle()
            rightKneeAngle = CalculatedAngles(frameMeasurement).calculateRightKneeAngle()
            leftShoulderAngle = CalculatedAngles(frameMeasurement).calculateLeftShoulderAngle()
            rightShoulderAngle = CalculatedAngles(frameMeasurement).calculateRightShoulderAngle()

            leftWristXCoordinate = None
            rightWristXCoordinate = None
            for measurement in frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.LEFT_WRIST:
                    leftWristXCoordinate = measurement.x
                elif measurement.landmark == LandmarkPosition.RIGHT_WRIST:
                    rightWristXCoordinate = measurement.x
                elif measurement.landmark == LandmarkPosition.LEFT_KNEE:
                    leftKneeCoordinate = measurement.x
                elif measurement.landmark == LandmarkPosition.RIGHT_KNEE:
                    rightKneeCoordinate = measurement.x

            # TODO: check if the arms are straightening first by measuring the elbow angles and the shoulder angle is increasing
            # else give feedback on arms: not straightening arms

            # TODO: make sure that the arms must moving first then the body will pivot after and before the leg bends
            # by making if the arm move then check if the hip angle is decreasing or not and check if the leg angle is still around 180
            # else give feedback: need to straighten the arms first / close the body / keep the leg straight

            # TODO: after 2 conditions above are met then check if the knee angles are decreasing and make sure the final knee angles is around 30
            # else give feedback: leg is not bent properly

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

        def recoveryTechniqueAnalyzer(self):
            raise NotImplementedError
