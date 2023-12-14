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

    def analyzeData(self, previousHipAngle, currentHipAngle, previousKneeAngle, currentKneeAngle):
        feedback = []
        if currentKneeAngle > previousKneeAngle:
            if previousHipAngle < currentHipAngle:
                feedback.append("Lean back when extending legs")

        elif currentKneeAngle < 150:
            feedback.append("Leg not fully extended")

        return feedback

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.RECOVERY_PHASE:
            (previousHipAngle, currentHipAngle, previousKneeAngle, currentKneeAngle) = self.extractData(normalizedFrameMeasurements)
            return self.analyzeData(previousHipAngle, currentHipAngle, previousKneeAngle, currentKneeAngle)
        return []
