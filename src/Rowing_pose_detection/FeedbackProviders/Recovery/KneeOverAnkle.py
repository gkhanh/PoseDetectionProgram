from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.models.Phase import Phase
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class KneeOverAnkle(RowingFeedbackProvider.FeedbackProvider):
    def extractData(self, normalizedFrameMeasurements):
        firstFrameMeasurement = normalizedFrameMeasurements[-5]
        lastFrameMeasurement = normalizedFrameMeasurements[-1]
        previousKneeAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateKneeAngle()
        currentKneeAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()

        # Initialize coordinates
        currentKneeXCoordinate = None
        currentAnkleXCoordinate = None

        # Extract coordinates from last frame
        for normalizedMeasurement in lastFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                currentKneeXCoordinate = normalizedMeasurement.x
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.ANKLE:
                currentAnkleXCoordinate = normalizedMeasurement.x

        return previousKneeAngle, currentKneeAngle, currentKneeXCoordinate, currentAnkleXCoordinate

    def analyzeData(self, currentKneeAngle, previousKneeAngle, currentKneeXCoordinate, currentAnkleXCoordinate):
        feedback = []

        if (currentKneeAngle is not None and previousKneeAngle is not None and currentKneeAngle < previousKneeAngle and
                currentKneeXCoordinate is not None and currentAnkleXCoordinate is not None and
                currentKneeXCoordinate < currentAnkleXCoordinate):
            feedback.append("Knee must go over ankle")
        return feedback

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.DRIVE_PHASE:
            previousKneeAngle, currentKneeAngle, currentKneeXCoordinate, currentAnkleXCoordinate = self.extractData(
                normalizedFrameMeasurements)

            return self.analyzeData(previousKneeAngle, currentKneeAngle, currentKneeXCoordinate,
                                    currentAnkleXCoordinate)
        return []
