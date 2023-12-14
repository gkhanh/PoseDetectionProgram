from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.Phase import Phase
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class BodyPosture(RowingFeedbackProvider.FeedbackProvider):

    def extractData(self, normalizedFrameMeasurements):
        firstFrameMeasurement = normalizedFrameMeasurements[-5]
        lastFrameMeasurement = normalizedFrameMeasurements[-1]
        previousHipAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateHipAngle()
        currentHipAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateHipAngle()
        previousElbowAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateElbowAngle()
        currentElbowAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateElbowAngle()
        return previousHipAngle, currentHipAngle, previousElbowAngle, currentElbowAngle

    def analyzeData(self, previousHipAngle, currentHipAngle, previousElbowAngle, currentElbowAngle):
        feedback = []
        if (
                currentElbowAngle is not None and previousElbowAngle is not None and currentElbowAngle > previousElbowAngle and
                previousHipAngle is not None and currentHipAngle is not None and currentHipAngle > previousHipAngle and
                not 60 < currentHipAngle < 80):
            feedback.append("Tip your body forward")
        return feedback

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.DRIVE_PHASE:
            (previousHipAngle, currentHipAngle, previousElbowAngle, currentElbowAngle) = self.extractData(
                normalizedFrameMeasurements)
            return self.analyzeData(previousHipAngle, currentHipAngle, previousElbowAngle, currentElbowAngle)
        return []
