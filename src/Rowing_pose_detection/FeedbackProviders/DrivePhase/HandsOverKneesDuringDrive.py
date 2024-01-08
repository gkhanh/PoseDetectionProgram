from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.models.Phase import Phase
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class HandsOverKneesDuringDrive(RowingFeedbackProvider.FeedbackProvider):

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.RECOVERY_PHASE:
            (lastShoulderAngleDuringDrive, lastElbowAngleDuringDrive, previousWristXCoordinateDuringDrive, 
             lastKneeXCoordinateDuringDrive, lastWristXCoordinateDuringDrive) = self.extractData(normalizedFrameMeasurements)
            return self.analyzeData(lastShoulderAngleDuringDrive, lastElbowAngleDuringDrive, previousWristXCoordinateDuringDrive,
                                    lastKneeXCoordinateDuringDrive, lastWristXCoordinateDuringDrive)

        return []

    def analyzeData(self, lastShoulderAngleDuringDrive, lastElbowAngleDuringDrive, previousWristXCoordinateDuringDrive, lastKneeXCoordinateDuringDrive,
                    lastWristXCoordinateDuringDrive):
        feedback = []
        if (lastShoulderAngleDuringDrive is not None and lastElbowAngleDuringDrive is not None
                and lastKneeXCoordinateDuringDrive is not None
                and lastWristXCoordinateDuringDrive is not None and previousWristXCoordinateDuringDrive is not None):
            if not lastKneeXCoordinateDuringDrive - 0.05 <= lastWristXCoordinateDuringDrive <= lastKneeXCoordinateDuringDrive + 0.05:
                if previousWristXCoordinateDuringDrive < lastWristXCoordinateDuringDrive:
                    feedback.append("Not pulling arm")
            if not lastShoulderAngleDuringDrive < 10 and 60 < lastElbowAngleDuringDrive <= 95:
                feedback.append("Arm not pulled back properly")
            if lastWristXCoordinateDuringDrive < lastKneeXCoordinateDuringDrive:
                feedback.append("Hands not over knees")

        return feedback

    def extractData(self, normalizedFrameMeasurements):
        firstFrameMeasurement = normalizedFrameMeasurements[-5]
        lastFrameMeasurement = normalizedFrameMeasurements[-1]
        lastShoulderAngleDuringDrive = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateShoulderAngle()
        lastElbowAngleDuringDrive = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateElbowAngle()
        previousWristXCoordinateDuringDrive = None
        lastKneeXCoordinateDuringDrive = None
        lastWristXCoordinateDuringDrive = None
        for normalizedMeasurement in firstFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                previousWristXCoordinateDuringDrive = normalizedMeasurement.x
        for normalizedMeasurement in lastFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                lastKneeXCoordinateDuringDrive = normalizedMeasurement.x
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                lastWristXCoordinateDuringDrive = normalizedMeasurement.x
        return lastShoulderAngleDuringDrive, lastElbowAngleDuringDrive, previousWristXCoordinateDuringDrive, lastKneeXCoordinateDuringDrive, lastWristXCoordinateDuringDrive
