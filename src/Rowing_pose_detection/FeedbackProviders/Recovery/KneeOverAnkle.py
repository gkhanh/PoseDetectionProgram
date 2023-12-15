from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.models.Phase import Phase
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class KneeOverAnkle(RowingFeedbackProvider.FeedbackProvider):
    def extractData(self, normalizedFrameMeasurements):
        firstFrameMeasurement = normalizedFrameMeasurements[-5]
        lastFrameMeasurement = normalizedFrameMeasurements[-1]
        previousKneeAngleDuringRecovery = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateKneeAngle()
        lastKneeAngleDuringRecovery = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()

        # Initialize coordinates
        lastKneeXCoordinateDuringRecovery = None
        lastAnkleXCoordinateDuringRecovery = None

        # Extract coordinates from last frame
        for normalizedMeasurement in lastFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                lastKneeXCoordinateDuringRecovery = normalizedMeasurement.x
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.ANKLE:
                lastAnkleXCoordinateDuringRecovery = normalizedMeasurement.x

        return previousKneeAngleDuringRecovery, lastKneeAngleDuringRecovery, lastKneeXCoordinateDuringRecovery, lastAnkleXCoordinateDuringRecovery

    def analyzeData(self, previousKneeAngleDuringRecovery, lastKneeAngleDuringRecovery, lastKneeXCoordinateDuringRecovery, lastAnkleXCoordinateDuringRecovery):
        feedback = []

        if (previousKneeAngleDuringRecovery is not None and lastKneeAngleDuringRecovery is not None and lastKneeAngleDuringRecovery < previousKneeAngleDuringRecovery and
                lastKneeXCoordinateDuringRecovery is not None and lastAnkleXCoordinateDuringRecovery is not None and not
                lastAnkleXCoordinateDuringRecovery - 0.04 < lastKneeXCoordinateDuringRecovery < lastAnkleXCoordinateDuringRecovery + 0.02):
            feedback.append("Knee must align with ankle")
        return feedback

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.DRIVE_PHASE:
            previousKneeAngleDuringRecovery, lastKneeAngleDuringRecovery, lastKneeXCoordinateDuringRecovery, lastAnkleXCoordinateDuringRecovery = self.extractData(
                normalizedFrameMeasurements)

            return self.analyzeData(previousKneeAngleDuringRecovery, lastKneeAngleDuringRecovery, lastKneeXCoordinateDuringRecovery, lastAnkleXCoordinateDuringRecovery)
        return []
