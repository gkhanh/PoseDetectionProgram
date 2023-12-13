from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.Phase import Phase
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class HandsOverKneesDuringDrive(RowingFeedbackProvider.FeedbackProvider):

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.RECOVERY_PHASE:
            # We went into the recovery, so the frameMeasurementBuffer contains the last drive
            # Check if the hands were over the knees during the drive
            firstFrameMeasurement = normalizedFrameMeasurements[-5]
            lastFrameMeasurement = normalizedFrameMeasurements[-1]
            currentShoulderAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateShoulderAngle()
            currentElbowAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateElbowAngle()
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
            if (currentShoulderAngle is not None and currentElbowAngle is not None
                    and currentKneeXCoordinate is not None
                    and currentWristXCoordinate is not None and previousWristXCoordinate is not None):
                if not currentKneeXCoordinate - 0.05 <= currentWristXCoordinate <= currentKneeXCoordinate + 0.05:
                    if previousWristXCoordinate < currentWristXCoordinate:
                        print("Feedback: Not pulling arm")
                        return ["Not pulling arm"]
                if not currentShoulderAngle < 10 and 60 < currentElbowAngle <= 95:
                    print("Feedback: Arm not pulled back properly")
                    return ["Arm not pulled back properly"]
        return []
