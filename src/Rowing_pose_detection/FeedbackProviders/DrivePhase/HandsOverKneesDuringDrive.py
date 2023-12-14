from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.models.Phase import Phase
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class HandsOverKneesDuringDrive(RowingFeedbackProvider.FeedbackProvider):

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.RECOVERY_PHASE:
            (currentShoulderAngle, currentElbowAngle, previousWristXCoordinate, currentKneeXCoordinate, currentWristXCoordinate) = self.extractData(normalizedFrameMeasurements)
            return self.analyzeData(currentShoulderAngle, currentElbowAngle, previousWristXCoordinate,
                                    currentKneeXCoordinate, currentWristXCoordinate)

        return []

    def analyzeData(self, currentShoulderAngle, currentElbowAngle, previousWristXCoordinate, currentKneeXCoordinate,
                    currentWristXCoordinate):
        feedback = []
        if (currentShoulderAngle is not None and currentElbowAngle is not None
                and currentKneeXCoordinate is not None
                and currentWristXCoordinate is not None and previousWristXCoordinate is not None):
            if not currentKneeXCoordinate - 0.05 <= currentWristXCoordinate <= currentKneeXCoordinate + 0.05:
                if previousWristXCoordinate < currentWristXCoordinate:
                    feedback.append("Not pulling arm")
            if not currentShoulderAngle < 10 and 60 < currentElbowAngle <= 95:
                feedback.append("Arm not pulled back properly")
        return feedback

    def extractData(self, normalizedFrameMeasurements):
        firstFrameMeasurement = normalizedFrameMeasurements[-5]
        lastFrameMeasurement = normalizedFrameMeasurements[-1]
        currentShoulderAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateShoulderAngle()
        currentElbowAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateElbowAngle()
        previousWristXCoordinate = None
        currentKneeXCoordinate = None
        currentWristXCoordinate = None
        for normalizedMeasurement in firstFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                previousWristXCoordinate = normalizedMeasurement.x
        for normalizedMeasurement in lastFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                currentKneeXCoordinate = normalizedMeasurement.x
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                currentWristXCoordinate = normalizedMeasurement.x
        return currentShoulderAngle, currentElbowAngle, previousWristXCoordinate, currentKneeXCoordinate, currentWristXCoordinate
