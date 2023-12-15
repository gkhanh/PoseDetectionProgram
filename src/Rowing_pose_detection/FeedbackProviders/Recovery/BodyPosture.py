from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.Phase import Phase
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class BodyPosture(RowingFeedbackProvider.FeedbackProvider):

    def extractData(self, normalizedFrameMeasurements):
        firstFrameMeasurement = normalizedFrameMeasurements[-5]
        lastFrameMeasurement = normalizedFrameMeasurements[-1]
        previousHipAngleDuringRecovery = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateHipAngle()
        lastHipAngleDuringRecovery = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateHipAngle()
        previousElbowAngleDuringRecovery = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateElbowAngle()
        lastElbowAngleDuringRecovery = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateElbowAngle()
        return previousHipAngleDuringRecovery, lastHipAngleDuringRecovery, previousElbowAngleDuringRecovery, lastElbowAngleDuringRecovery

    def analyzeData(self, previousHipAngleDuringRecovery, lastHipAngleDuringRecovery, previousElbowAngleDuringRecovery, lastElbowAngleDuringRecovery):
        feedback = []
        if (
                lastElbowAngleDuringRecovery is not None and previousElbowAngleDuringRecovery is not None and lastElbowAngleDuringRecovery > previousElbowAngleDuringRecovery and
                previousHipAngleDuringRecovery is not None and lastHipAngleDuringRecovery is not None and lastHipAngleDuringRecovery < previousHipAngleDuringRecovery and
                not 60 < lastHipAngleDuringRecovery < 80):
            feedback.append("Tip your body forward")
        return feedback

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.DRIVE_PHASE:
            (previousHipAngleDuringRecovery, lastHipAngleDuringRecovery, previousElbowAngleDuringRecovery, lastElbowAngleDuringRecovery) = self.extractData(
                normalizedFrameMeasurements)
            return self.analyzeData(previousHipAngleDuringRecovery, lastHipAngleDuringRecovery, previousElbowAngleDuringRecovery, lastElbowAngleDuringRecovery)
        return []
