from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.models.Phase import Phase
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class ArmAndLegMovement(RowingFeedbackProvider.FeedbackProvider):

    def extractData(self, normalizedFrameMeasurements):
        firstFrameMeasurement = normalizedFrameMeasurements[-5]
        lastFrameMeasurement = normalizedFrameMeasurements[-1]
        currentElbowAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateElbowAngle()
        currentKneeAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()
        currentKneeXCoordinate = None
        previousWristXCoordinate = None
        currentWristXCoordinate = None

        for normalizedMeasurement in firstFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                previousWristXCoordinate = normalizedMeasurement.x

        for normalizedMeasurement in lastFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                currentKneeXCoordinate = normalizedMeasurement.x
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                currentWristXCoordinate = normalizedMeasurement.x

        return (currentElbowAngle, currentKneeAngle,
                currentKneeXCoordinate, previousWristXCoordinate, currentWristXCoordinate)

    def analyzeData(self, currentElbowAngle, currentKneeAngle,
                    currentKneeXCoordinate, previousWristXCoordinate, currentWristXCoordinate):
        feedback = []
        if currentWristXCoordinate is not None and previousWristXCoordinate is not None and currentWristXCoordinate > previousWristXCoordinate:
            feedback.append("Move the handle forward")
        elif currentKneeAngle is not None and 150 < currentKneeAngle <= 180:
            if currentElbowAngle is not None and currentElbowAngle < 150:
                feedback.append("Straighten the arm")
            elif currentWristXCoordinate is not None and currentKneeXCoordinate is not None and currentWristXCoordinate < currentKneeXCoordinate:
                feedback.append("Straighten arms until hands over knees")
        return feedback

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.DRIVE_PHASE:
            (currentElbowAngle, currentKneeAngle,
             currentKneeXCoordinate, previousWristXCoordinate, currentWristXCoordinate) = self.extractData(
                normalizedFrameMeasurements)
            return self.analyzeData(currentElbowAngle, currentKneeAngle,
                                    currentKneeXCoordinate, previousWristXCoordinate, currentWristXCoordinate)
        return []
