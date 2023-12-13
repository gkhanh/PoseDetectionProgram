from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.models.Phase import Phase
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.utils.CalculateAnglesWithNormalizedData import CalculateAnglesWithNormalizedData


class KneeOverAnkle(RowingFeedbackProvider.FeedbackProvider):
    def getFeedback(self, currentPhase, normalizedFrameMeasurements):
        if currentPhase == Phase.DRIVE_PHASE:
            # We went into the recovery, so the frameMeasurementBuffer contains the last drive
            firstFrameMeasurement = normalizedFrameMeasurements[-5]
            lastFrameMeasurement = normalizedFrameMeasurements[-1]

            previousKneeAngle = CalculateAnglesWithNormalizedData(firstFrameMeasurement).calculateKneeAngle()
            currentKneeAngle = CalculateAnglesWithNormalizedData(lastFrameMeasurement).calculateKneeAngle()

            previousKneeXCoordinate = None
            previousAnkleXCoordinate = None
            currentKneeXCoordinate = None
            currentAnkleXCoordinate = None

            for normalizedMeasurement in firstFrameMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                    currentKneeXCoordinate = normalizedMeasurement.x
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.ANKLE:
                    previousAnkleXCoordinate = normalizedMeasurement.x
            for normalizedMeasurement in lastFrameMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                    currentKneeXCoordinate = normalizedMeasurement.x
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.ANKLE:
                    currentAnkleXCoordinate = normalizedMeasurement.x

            if currentKneeAngle is not None and previousKneeAngle is not None and currentKneeAngle < previousKneeAngle:
                if (currentKneeXCoordinate is not None and currentAnkleXCoordinate is not None and
                        currentKneeXCoordinate < currentAnkleXCoordinate):
                    print("Knee must go over ankle")
                    return ["Knee must go over ankle"]

        return []