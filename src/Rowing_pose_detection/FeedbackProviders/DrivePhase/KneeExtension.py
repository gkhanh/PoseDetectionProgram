from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.Phase import Phase
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class KneeExtension(RowingFeedbackProvider.FeedbackProvider):

    def extractData(self, normalizedFrameMeasurements):
        firstFrameMeasurement = normalizedFrameMeasurements[-5]
        lastFrameMeasurement = normalizedFrameMeasurements[-1]
        previousHipAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateHipAngle()
        currentHipAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateHipAngle()
        previousKneeAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateKneeAngle()
        currentKneeAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()
        return previousHipAngle, currentHipAngle, previousKneeAngle, currentKneeAngle

    def analyzeData(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.RECOVERY_PHASE:
            previousHipAngle, currentHipAngle, previousKneeAngle, currentKneeAngle = self.extractData(
                normalizedFrameMeasurements)

            while currentKneeAngle > previousKneeAngle:
                if previousHipAngle < currentHipAngle:
                    return ["Lean back when extending legs"]

            if currentKneeAngle < 150:
                return ["Leg not fully extended"]

        return []

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        return self.analyzeData(currentPhase, normalizedFrameMeasurements)