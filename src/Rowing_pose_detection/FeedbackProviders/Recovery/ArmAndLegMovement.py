from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.models.Phase import Phase
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class ArmAndLegMovement(RowingFeedbackProvider.FeedbackProvider):

    def extractData(self, normalizedFrameMeasurements):
        firstFrameMeasurement = normalizedFrameMeasurements[-5]
        lastFrameMeasurement = normalizedFrameMeasurements[-1]
        lastElbowAngleDuringRecovery = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateElbowAngle()
        previousElbowAngleDuringRecovery = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateElbowAngle()
        lastKneeAngleDuringRecovery = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()
        previousKneeAngleDuringRecovery = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateKneeAngle()
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

        return (lastElbowAngleDuringRecovery, previousElbowAngleDuringRecovery, lastKneeAngleDuringRecovery, previousKneeAngleDuringRecovery,
                lastKneeXCoordinateDuringRecovery, previousWristXCoordinateDuringRecovery,
                lastWristXCoordinateDuringRecovery)

    def analyzeData(self, lastElbowAngleDuringRecovery, previousElbowAngleDuringRecovery, lastKneeAngleDuringRecovery, previousKneeAngleDuringRecovery,
                    lastKneeXCoordinateDuringRecovery, previousWristXCoordinateDuringRecovery,
                    lastWristXCoordinateDuringRecovery):
        feedback = []
        if (lastWristXCoordinateDuringRecovery is not None and previousWristXCoordinateDuringRecovery is not None and
                lastElbowAngleDuringRecovery is not None and previousElbowAngleDuringRecovery is not None):
            if lastWristXCoordinateDuringRecovery > previousWristXCoordinateDuringRecovery and previousElbowAngleDuringRecovery > lastElbowAngleDuringRecovery:
                feedback.append("Move the handle forward")
        elif lastKneeAngleDuringRecovery is not None and 150 < lastKneeAngleDuringRecovery <= 180:
            if lastElbowAngleDuringRecovery is not None and lastElbowAngleDuringRecovery < 150:
                feedback.append("Straighten the arm")
            elif lastWristXCoordinateDuringRecovery is not None and lastKneeXCoordinateDuringRecovery is not None and lastWristXCoordinateDuringRecovery < lastKneeXCoordinateDuringRecovery:
                feedback.append("Straighten arms until hands over knees")
        if previousKneeAngleDuringRecovery is not None and lastKneeAngleDuringRecovery is not None and lastElbowAngleDuringRecovery is not None:
            if previousKneeAngleDuringRecovery > lastKneeAngleDuringRecovery and 30 < lastElbowAngleDuringRecovery < 90:
                feedback.append("Straighten arms before bend your knees")

        return feedback

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.DRIVE_PHASE:
            (lastElbowAngleDuringRecovery, previousElbowAngleDuringRecovery, lastKneeAngleDuringRecovery, previousKneeAngleDuringRecovery,
             lastKneeXCoordinateDuringRecovery, previousWristXCoordinateDuringRecovery,
             lastWristXCoordinateDuringRecovery) = self.extractData(
                normalizedFrameMeasurements)
            return self.analyzeData(lastElbowAngleDuringRecovery, previousElbowAngleDuringRecovery, lastKneeAngleDuringRecovery, previousKneeAngleDuringRecovery,
                                    lastKneeXCoordinateDuringRecovery, previousWristXCoordinateDuringRecovery,
                                    lastWristXCoordinateDuringRecovery)
        return []
