from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.Phase import Phase
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class KneeOverAnkle(RowingFeedbackProvider.FeedbackProvider):
    def extractData(self, normalizedFrameMeasurements):
        firstFrameMeasurement = normalizedFrameMeasurements[-5]
        lastFrameMeasurement = normalizedFrameMeasurements[-1]
        previousKneeAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateKneeAngle()
        currentKneeAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()

        # Initialize coordinates
        previousKneeXCoordinate = previousAnkleXCoordinate = currentKneeXCoordinate = currentAnkleXCoordinate = None

        # Extract coordinates from first frame
        for normalizedMeasurement in firstFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                previousKneeXCoordinate = normalizedMeasurement.x
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.ANKLE:
                previousAnkleXCoordinate = normalizedMeasurement.x

        # Extract coordinates from last frame
        for normalizedMeasurement in lastFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                currentKneeXCoordinate = normalizedMeasurement.x
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.ANKLE:
                currentAnkleXCoordinate = normalizedMeasurement.x

        return previousKneeAngle, currentKneeAngle, previousKneeXCoordinate, previousAnkleXCoordinate, currentKneeXCoordinate, currentAnkleXCoordinate

    def analyzeData(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.DRIVE_PHASE:
            previousKneeAngle, currentKneeAngle, previousKneeXCoordinate, previousAnkleXCoordinate, currentKneeXCoordinate, currentAnkleXCoordinate = self.extractData(
                normalizedFrameMeasurements)
            if (
                    currentKneeAngle is not None and previousKneeAngle is not None and currentKneeAngle < previousKneeAngle and
                    currentKneeXCoordinate is not None and currentAnkleXCoordinate is not None and
                    currentKneeXCoordinate < currentAnkleXCoordinate):
                return ["Knee must go over ankle"]
        return []

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        return self.analyzeData(currentPhase, normalizedFrameMeasurements)