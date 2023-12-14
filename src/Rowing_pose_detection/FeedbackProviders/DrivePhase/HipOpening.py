from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.Phase import Phase
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class HipOpening(RowingFeedbackProvider.FeedbackProvider):

    def extractData(self, normalizedFrameMeasurements):
        firstFrameMeasurement = normalizedFrameMeasurements[-5]
        lastFrameMeasurement = normalizedFrameMeasurements[-1]
        previousHipAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateHipAngle()
        currentHipAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateHipAngle()
        previousKneeAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateKneeAngle()
        currentKneeAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()
        return currentKneeAngle, currentHipAngle, previousHipAngle

    def analyzeData(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.RECOVERY_PHASE:
            currentKneeAngle, currentHipAngle, previousHipAngle = self.extractData(normalizedFrameMeasurements)
            if currentKneeAngle < 150 and currentHipAngle >= 90:
                return ["Open hip too soon"]
            elif currentHipAngle <= 100 and not previousHipAngle < currentHipAngle:
                return ["Hip is not open"]
        return []

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        return self.analyzeData(currentPhase, normalizedFrameMeasurements)