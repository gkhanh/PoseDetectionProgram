from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.Phase import Phase
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class HipOpening(RowingFeedbackProvider.FeedbackProvider):

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.RECOVERY_PHASE:
            (currentKneeAngle, currentHipAngle, previousHipAngle) = self.extractData(normalizedFrameMeasurements)
            return self.analyzeData(currentKneeAngle, currentHipAngle, previousHipAngle)
        return []

    def analyzeData(self, currentKneeAngle, currentHipAngle, previousHipAngle):
        feedback = []
        if currentKneeAngle is not None and currentHipAngle is not None and previousHipAngle is not None:
            if currentKneeAngle < 150 and currentHipAngle >= 90:
                feedback.append("Open hip too soon")
            elif currentHipAngle <= 100 and not previousHipAngle < currentHipAngle:
                feedback.append("Hip is not open")
        return feedback

    def extractData(self, normalizedFrameMeasurements):
        firstFrameMeasurement = normalizedFrameMeasurements[-5]
        lastFrameMeasurement = normalizedFrameMeasurements[-1]
        previousHipAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateHipAngle()
        currentHipAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateHipAngle()
        currentKneeAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()
        return currentKneeAngle, currentHipAngle, previousHipAngle
