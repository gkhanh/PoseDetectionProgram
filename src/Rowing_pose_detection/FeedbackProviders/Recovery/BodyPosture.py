from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.Phase import Phase
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class BodyPosture(RowingFeedbackProvider.FeedbackProvider):

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.DRIVE_PHASE:
            # We went into the recovery, so the frameMeasurementBuffer contains the last drive
            firstFrameMeasurement = normalizedFrameMeasurements[-5]
            lastFrameMeasurement = normalizedFrameMeasurements[-1]

            previousHipAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateHipAngle()
            currentHipAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateHipAngle()

            currentElbowAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateElbowAngle()
            previousElbowAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateElbowAngle()

            if currentElbowAngle is not None and previousElbowAngle is not None and currentElbowAngle > previousElbowAngle:
                if (previousHipAngle is not None and currentHipAngle is not None and currentHipAngle > previousHipAngle and
                        not 60 < currentHipAngle < 80):
                    print("Tip your body forward")
                    return ["Tip your body forward"]

        return []



