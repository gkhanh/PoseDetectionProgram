from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.Phase import Phase
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class ArmAndLegMovement(RowingFeedbackProvider.FeedbackProvider):

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.DRIVE_PHASE:
            # We went into the recovery, so the frameMeasurementBuffer contains the last drive
            firstFrameMeasurement = normalizedFrameMeasurements[-5]
            lastFrameMeasurement = normalizedFrameMeasurements[-1]

            previousElbowAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateElbowAngle()
            currentElbowAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateElbowAngle()

            previousHipAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateHipAngle()
            currentHipAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateHipAngle()

            previousKneeAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateKneeAngle()
            currentKneeAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()

            previousKneeXCoordinate = None
            previousWristXCoordinate = None
            currentKneeXCoordinate = None
            currentWristXCoordinate = None

            for normalizedMeasurement in firstFrameMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                    currentKneeXCoordinate = normalizedMeasurement.x
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                    previousWristXCoordinate = normalizedMeasurement.x
            for normalizedMeasurement in lastFrameMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                    currentKneeXCoordinate = normalizedMeasurement.x
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                    currentWristXCoordinate = normalizedMeasurement.x

            if currentWristXCoordinate is not None and previousWristXCoordinate is not None and currentWristXCoordinate > previousWristXCoordinate:
                print("Feedback: Move the handle forward")
                return ["Move the handle forward"]
            else:
                if currentKneeAngle is not None and 150 < currentKneeAngle <= 180:
                    print("Feedback: Straighten knees until hands over knees")
                    return ["Straighten knees until hands over knees"]
        return []
