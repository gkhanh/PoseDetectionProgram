from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.Phase import Phase


class HandsOverKneesDuringDrive(RowingFeedbackProvider.FeedbackProvider):

    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.RECOVERY_PHASE:
            # We went into the recovery, so the frameMeasurementBuffer contains the last drive
            # Check if the hands were over the knees during the drive
            # TODO: Implement
            pass

        return []
