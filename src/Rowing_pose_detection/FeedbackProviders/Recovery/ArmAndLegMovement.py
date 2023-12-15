from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.models.Phase import Phase
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class ArmAndLegMovement(RowingFeedbackProvider.FeedbackProvider):

    def extractData(self, normalizedFrameMeasurements):
        firstFrameMeasurement = normalizedFrameMeasurements[-5]
        lastFrameMeasurement = normalizedFrameMeasurements[-1]
        lastElbowAngleDuringRecovery = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateElbowAngle()
        lastKneeAngleDuringRecovery = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()
        lastKneeXCoordinateDuringRecovery = None
        previousWristXCoordinateDuringRecovery = None
        lastWristXCoordinateDuringRecovery = None

        for normalizedMeasurement in firstFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                previousWristXCoordinateDuringRecovery = normalizedMeasurement.x

        for normalizedMeasurement in lastFrameMeasurement.normalizedMeasurements:
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                lastKneeXCoordinateDuringRecovery = normalizedMeasurement.x
            if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                lastWristXCoordinateDuringRecovery = normalizedMeasurement.x

        return (lastElbowAngleDuringRecovery, lastKneeAngleDuringRecovery,
                lastKneeXCoordinateDuringRecovery, previousWristXCoordinateDuringRecovery,
                lastWristXCoordinateDuringRecovery)

    def analyzeData(self, lastElbowAngleDuringRecovery, lastKneeAngleDuringRecovery,
                    lastKneeXCoordinateDuringRecovery, previousWristXCoordinateDuringRecovery,
                    lastWristXCoordinateDuringRecovery):
        feedback = []
        if lastWristXCoordinateDuringRecovery is not None and previousWristXCoordinateDuringRecovery is not None and lastWristXCoordinateDuringRecovery > previousWristXCoordinateDuringRecovery:
            feedback.append("Move the handle forward")
        elif lastKneeAngleDuringRecovery is not None and 150 < lastKneeAngleDuringRecovery <= 180:
            if lastElbowAngleDuringRecovery is not None and lastElbowAngleDuringRecovery < 150:
                feedback.append("Straighten the arm")
            elif lastWristXCoordinateDuringRecovery is not None and lastKneeXCoordinateDuringRecovery is not None and lastWristXCoordinateDuringRecovery < lastKneeXCoordinateDuringRecovery:
                feedback.append("Straighten arms until hands over knees")
        return feedback

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.DRIVE_PHASE:
            (lastElbowAngleDuringRecovery, lastKneeAngleDuringRecovery,
             lastKneeXCoordinateDuringRecovery, previousWristXCoordinateDuringRecovery,
             lastWristXCoordinateDuringRecovery) = self.extractData(
                normalizedFrameMeasurements)
            return self.analyzeData(lastElbowAngleDuringRecovery, lastKneeAngleDuringRecovery,
                                    lastKneeXCoordinateDuringRecovery, previousWristXCoordinateDuringRecovery,
                                    lastWristXCoordinateDuringRecovery)
        return []
