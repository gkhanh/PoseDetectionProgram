from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.Phase import Phase
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class ArmAndLegMovement(RowingFeedbackProvider.FeedbackProvider):

    def extractData(self, normalizedFrameMeasurements):
        firstFrameMeasurement = normalizedFrameMeasurements[-5]
        lastFrameMeasurement = normalizedFrameMeasurements[-1]
        previousElbowAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateElbowAngle()
        currentElbowAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateElbowAngle()
        previousHipAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateHipAngle()
        currentHipAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateHipAngle()
        previousKneeAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateKneeAngle()
        currentKneeAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()
        previousKneeXCoordinate, previousWristXCoordinate = self.getCoordinates(firstFrameMeasurement)
        currentKneeXCoordinate, currentWristXCoordinate = self.getCoordinates(lastFrameMeasurement)
        return (previousElbowAngle, currentElbowAngle, previousHipAngle, currentHipAngle, previousKneeAngle, currentKneeAngle,
                previousKneeXCoordinate, previousWristXCoordinate, currentKneeXCoordinate, currentWristXCoordinate)

    def getCoordinates(self, frameMeasurement):
        kneeXCoordinate, wristXCoordinate = None, None
        for normalizedMeasurement in frameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                kneeXCoordinate = normalizedMeasurement.x
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                wristXCoordinate = normalizedMeasurement.x
        return kneeXCoordinate, wristXCoordinate

    def analyzeData(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.DRIVE_PHASE:
            (previousElbowAngle, currentElbowAngle, previousHipAngle, currentHipAngle, previousKneeAngle, currentKneeAngle,
             previousKneeXCoordinate, previousWristXCoordinate, currentKneeXCoordinate, currentWristXCoordinate) = self.extractData(normalizedFrameMeasurements)

            if currentWristXCoordinate is not None and previousWristXCoordinate is not None and currentWristXCoordinate > previousWristXCoordinate:
                return ["Move the handle forward"]
            else:
                if currentKneeAngle is not None and 150 < currentKneeAngle <= 180:
                    return ["Straighten knees until hands over knees"]

        return []

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        return self.analyzeData(currentPhase, normalizedFrameMeasurements)
