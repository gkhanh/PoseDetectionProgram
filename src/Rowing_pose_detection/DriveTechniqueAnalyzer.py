from src.models.Phase import Phase
from src.pose_detection.PoseDetector import PoseDetector
from src.utils.CalculatedAngles import CalculatedAngles
from src.utils.Cancellable import Cancellable
from src.models.measurement import LandmarkPosition
from src.Rowing_pose_detection.PhaseDetector import PhaseDetector


class DriveTechniqueAnalyzer(PhaseDetector.Listener, PoseDetector.Listener):
    def __init__(self, phaseDetector, poseDetector, frameMeasurementBuffer):
        self.frameMeasurementBuffer = frameMeasurementBuffer
        self.poseDetector = poseDetector

        # for Listeners
        self.poseDetectorCancellable = None
        self.phaseDetectorCancellable = None
        self.listeners = []

        self.currentPhase = phaseDetector.currentPhase

    def onPhaseChange(self, currentPhase, frameMeasurementBuffer):
        if currentPhase == Phase.DRIVE_PHASE:
            if self.poseDetectorCancellable is None:
                self.poseDetectorCancellable = self.poseDetector.addListener(self)
        else:
            if self.poseDetectorCancellable is not None:
                self.poseDetectorCancellable.cancel()

    def onMeasurement(self, frameMeasurement):
        self.frameMeasurementBuffer.append(frameMeasurement)
        self.drivePhaseTechniqueAnalyzer()

    def drivePhaseTechniqueAnalyzer(self):
        for frameMeasurement in self.frameMeasurementBuffer:
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
            leftKneeCoordinate = None
            rightKneeCoordinate = None
            for measurement in frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.LEFT_WRIST:
                    leftWristXCoordinate = measurement.x
                elif measurement.landmark == LandmarkPosition.RIGHT_WRIST:
                    rightWristXCoordinate = measurement.x
                elif measurement.landmark == LandmarkPosition.LEFT_KNEE:
                    leftKneeCoordinate = measurement.x
                elif measurement.landmark == LandmarkPosition.RIGHT_KNEE:
                    rightKneeCoordinate = measurement.x

        # TODO: measure the knee angles, check if the knees angles is less than 100 degree, then the hip angles has to be stay less than 90 degree
        # else give feedback on hip: open hip too soon

        # TODO: measure the hip angles, check if the knees angles is more than 100 degree, then check if the hip angles is increasing or not
        # else give feedback on hip opening: not opening hip

        # TODO: check if the knee angles is around 180 degree (fully extended) and hip angles is more than 100 degree
        # else give feedback on hip opening: not opening hip, leg not fully extended

        # TODO: check when the user can pull back the arm by comparing the x coordinates of both wrists and knees, if they are equal
        # else give feedback: pull arm too soon/early

        # TODO: check if the previous condition is met, then check the x coordinates of both wrists if its decreasing(?) and shoulder angle is decreasing
        # else give feedback: arm not pulled back

        # TODO: check if the arms are fully pulled back by checking the shoulder angla is less than 10 degree and elbow angles is around 90 degree
        # else give feedback: arm not pulled back properly

    def addListener(self, listener):
        self.listeners.append(listener)
        if len(self.listeners) == 1:
            self.phaseDetectorCancellable = self.phaseDetector.addListener(self)
        return Cancellable(lambda: self._removeListener(listener))

    def _removeListener(self, listener):
        self.listeners.remove(listener)
        if len(self.listeners) == 0 and self.phaseDetectorCancellable is not None:
            self.phaseDetectorCancellable.cancel()

    def notifyListeners(self, frameMeasurementBuffer):
        for listener in self.listeners:
            listener.onPhaseChange(self.currentPhase, frameMeasurementBuffer)

    class Listener:

        def driveTechniqueAnalyzer(self):
            raise NotImplementedError
