from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.Phase import Phase
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class KneeExtension(RowingFeedbackProvider.FeedbackProvider):

    def extractData(self, normalizedFrameMeasurements):
        firstFrameMeasurement = normalizedFrameMeasurements[-5]
        lastFrameMeasurement = normalizedFrameMeasurements[-1]
        previousHipAngleDuringDrive = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateHipAngle()
        lastHipAngleDuringDrive = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateHipAngle()
        previousKneeAngleDuringDrive = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateKneeAngle()
        lastKneeAngleDuringDrive = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()
        return previousHipAngleDuringDrive, lastHipAngleDuringDrive, previousKneeAngleDuringDrive, lastKneeAngleDuringDrive

    def analyzeData(self, previousHipAngleDuringDrive, lastHipAngleDuringDrive, previousKneeAngleDuringDrive, lastKneeAngleDuringDrive):
        feedback = []
        if lastKneeAngleDuringDrive is not None and previousKneeAngleDuringDrive is not None and lastKneeAngleDuringDrive > previousKneeAngleDuringDrive:
            if previousKneeAngleDuringDrive >= 150 and 60 <= lastHipAngleDuringDrive < previousHipAngleDuringDrive <= 90:
                feedback.append("Keep your back straight when extending legs")

        if lastKneeAngleDuringDrive < 150:
            feedback.append("Legs not fully extended")

        return feedback

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.RECOVERY_PHASE:
            (previousHipAngleDuringDrive, lastHipAngleDuringDrive, previousKneeAngleDuringDrive, lastKneeAngleDuringDrive) = self.extractData(normalizedFrameMeasurements)
            return self.analyzeData(previousHipAngleDuringDrive, lastHipAngleDuringDrive, previousKneeAngleDuringDrive, lastKneeAngleDuringDrive)
        return []
