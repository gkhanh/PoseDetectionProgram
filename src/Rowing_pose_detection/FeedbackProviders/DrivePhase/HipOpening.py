from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.Phase import Phase
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class HipOpening(RowingFeedbackProvider.FeedbackProvider):

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.RECOVERY_PHASE:
            # We went into the recovery, so the frameMeasurementBuffer contains the last drive
            firstFrameMeasurement = normalizedFrameMeasurements[-5]
            lastFrameMeasurement = normalizedFrameMeasurements[-1]

            previousHipAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateHipAngle()
            currentHipAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateHipAngle()

            previousKneeAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateKneeAngle()
            currentKneeAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()

            if currentKneeAngle < 140 and currentHipAngle >= 90:
                print("Feedback: Open hip too soon")
                return ["Open hip too soon"]
            elif currentHipAngle <= 100 and not previousHipAngle < currentHipAngle:
                print("Feedback: Hip is not open")
                return ["Hip is not open"]
            # measure the hip angles, check if the knees angles is more than 100 degree, then check if the hip angles is
            # increasing or not, else give feedback on hip opening: not opening hip

        return []
