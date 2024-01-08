from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.Phase import Phase
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class HipOpening(RowingFeedbackProvider.FeedbackProvider):

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.RECOVERY_PHASE:
            (lastKneeAngleDuringDrive, lastHipAngleDuringDrive, previousHipAngleDuringDrive) = self.extractData(normalizedFrameMeasurements)
            return self.analyzeData(lastKneeAngleDuringDrive, lastHipAngleDuringDrive, previousHipAngleDuringDrive)
        return []

    def analyzeData(self, lastKneeAngleDuringDrive, lastHipAngleDuringDrive, previousHipAngleDuringDrive):
        feedback = []
        if lastKneeAngleDuringDrive is not None and lastHipAngleDuringDrive is not None and previousHipAngleDuringDrive is not None:
            if lastKneeAngleDuringDrive < 150 and lastHipAngleDuringDrive >= 90:
                feedback.append("Open hip too soon")
            elif lastHipAngleDuringDrive <= 100 and not previousHipAngleDuringDrive > lastHipAngleDuringDrive:
                feedback.append("Hip is not open")
        return feedback

    def extractData(self, normalizedFrameMeasurements):
        firstFrameMeasurement = normalizedFrameMeasurements[-5]
        lastFrameMeasurement = normalizedFrameMeasurements[-1]
        previousHipAngleDuringDrive = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateHipAngle()
        lastHipAngleDuringDrive = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateHipAngle()
        lastKneeAngleDuringDrive = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()
        return lastKneeAngleDuringDrive, lastHipAngleDuringDrive, previousHipAngleDuringDrive
