from src.exception.EmptyDataException import EmptyDataException
from src.utils.MathUtils import MathUtils
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition


class CalculateAnglesWithNormalizedData:
    def __init__(self, normalizedframeMeasurement) -> None:
        self.normalizedframeMeasurement = normalizedframeMeasurement
        self.operation = MathUtils()

    def calculateShoulderAngle(self):
        try:
            # Find the SHOULDER
            shoulderMeasurement = None
            if not self.normalizedframeMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in self.normalizedframeMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.SHOULDER:
                    shoulderMeasurement = normalizedMeasurement
                    break
            if shoulderMeasurement is None:
                return None

            # Find the ELBOW
            elbowMeasurement = None
            if not self.normalizedframeMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in self.normalizedframeMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.ELBOW:
                    elbowMeasurement = normalizedMeasurement
                    break
            if elbowMeasurement is None:
                return None

            # Find the HIP
            hipMeasurement = None
            if not self.normalizedframeMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in self.normalizedframeMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.HIP:
                    hipMeasurement = normalizedMeasurement
                    break
            if hipMeasurement is None:
                return None

            # Raise error if one of the measurements is missing
            if shoulderMeasurement is None or elbowMeasurement is None or hipMeasurement is None:
                raise EmptyDataException("Not enough data to calculate right shoulder angle")

            shoulderAngle = self.operation.calculateAngle(
                (hipMeasurement.x, hipMeasurement.y),
                (shoulderMeasurement.x, shoulderMeasurement.y),
                (elbowMeasurement.x, elbowMeasurement.y),
            )
            return round(shoulderAngle, 2)
        except AttributeError:
            return None

    def calculateElbowAngle(self):
        try:
            # Find the SHOULDER
            shoulderMeasurement = None
            if not self.normalizedframeMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in self.normalizedframeMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.SHOULDER:
                    rightShoulderMeasurement = normalizedMeasurement
                    break
            if shoulderMeasurement is None:
                return None

            # Find the ELBOW
            elbowMeasurement = None
            if not self.normalizedframeMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in self.normalizedframeMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.ELBOW:
                    elbowMeasurement = normalizedMeasurement
                    break
            if elbowMeasurement is None:
                return None

            # Find the WRIST
            wristMeasurement = None
            if not self.normalizedframeMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in self.normalizedframeMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                    wristMeasurement = normalizedMeasurement
                    break
            if wristMeasurement is None:
                return None

            # Raise error if one of the measurements is missing
            if shoulderMeasurement is None or elbowMeasurement is None or wristMeasurement is None:
                raise EmptyDataException("Not enough data to calculate right shoulder angle")

            elbowAngle = self.operation.calculateAngle(
                (wristMeasurement.x, wristMeasurement.y),
                (elbowMeasurement.x, elbowMeasurement.y),
                (shoulderMeasurement.x, shoulderMeasurement.y),
            )
            return round(elbowAngle, 2)
        except AttributeError:
            return None

    def calculateHandAngle(self):
        try:
            # Find the WRIST
            wristMeasurement = None
            if not self.normalizedframeMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in self.normalizedframeMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.WRIST:
                    wristMeasurement = normalizedMeasurement
                    break
            if wristMeasurement is None:
                return None

            # Find the INDEX
            indexMeasurement = None
            if not self.normalizedframeMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in self.normalizedframeMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.INDEX:
                    indexMeasurement = normalizedMeasurement
                    break
            if indexMeasurement is None:
                return None

            # Find the THUMB
            thumbMeasurement = None
            if not self.normalizedframeMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in self.normalizedframeMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.THUMB:
                    thumbMeasurement = normalizedMeasurement
                    break
            if thumbMeasurement is None:
                return None

            # Raise error if one of the measurements is missing
            if wristMeasurement is None or indexMeasurement is None or thumbMeasurement is None:
                raise EmptyDataException("Not enough data to calculate right elbow angle")

            elbowAngle = self.operation.calculateAngle(
                (indexMeasurement.x, indexMeasurement.y),
                (wristMeasurement.x, wristMeasurement.y),
                (thumbMeasurement.x, thumbMeasurement.y),
            )
            return round(elbowAngle, 2)
        except AttributeError:
            return None

    def calculateHipAngle(self):
        try:
            # Find the KNEE
            kneeMeasurement = None
            if not self.normalizedframeMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in self.normalizedframeMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                    kneeMeasurement = normalizedMeasurement
                    break
            if kneeMeasurement is None:
                return None

            # Find the HIP
            hipMeasurement = None
            if not self.normalizedframeMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in self.normalizedframeMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.HIP:
                    hipMeasurement = normalizedMeasurement
                    break
            if hipMeasurement is None:
                return None

            # Find the SHOULDER
            shoulderMeasurement = None
            if not self.normalizedframeMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in self.normalizedframeMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.SHOULDER:
                    shoulderMeasurement = normalizedMeasurement
                    break
            if shoulderMeasurement is None:
                return None

            hipAngle = self.operation.calculateAngle(
                (shoulderMeasurement.x, shoulderMeasurement.y),
                (hipMeasurement.x, hipMeasurement.y),
                (kneeMeasurement.x, kneeMeasurement.y),
            )
            return round(hipAngle, 2)
        except AttributeError:
            return None

    def calculateKneeAngle(self):
        try:
            # Find the KNEE
            kneeMeasurement = None
            if not self.normalizedframeMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in self.normalizedframeMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.KNEE:
                    kneeMeasurement = normalizedMeasurement
                    break
            if kneeMeasurement is None:
                return None

            # Find the ANKLE
            ankleMeasurement = None
            if not self.normalizedframeMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in self.normalizedframeMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.ANKLE:
                    ankleMeasurement = normalizedMeasurement
                    break
            if ankleMeasurement is None:
                return None

            # Find the HIP
            hipMeasurement = None
            if not self.normalizedframeMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in self.normalizedframeMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.HIP:
                    hipMeasurement = normalizedMeasurement
                    break
            if hipMeasurement is None:
                return None

            # Raise error if one of the measurements is missing
            if kneeMeasurement is None or hipMeasurement is None or ankleMeasurement is None:
                raise EmptyDataException("Not enough data to calculate knee angle")

            kneeAngle = self.operation.calculateAngle(
                (hipMeasurement.x, hipMeasurement.y),
                (kneeMeasurement.x, kneeMeasurement.y),
                (ankleMeasurement.x, ankleMeasurement.y),
            )
            return round(kneeAngle, 2)

        except AttributeError:
            return None

    def calculateFootAngle(self):
        try:
            # Find the FOOT_INDEX
            footIndexMeasurement = None
            if not self.normalizedframeMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in self.normalizedframeMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.FOOT_INDEX:
                    footIndexMeasurement = normalizedMeasurement
                    break
            if footIndexMeasurement is None:
                return None

            # Find the HEEL
            heelMeasurement = None
            if not self.normalizedframeMeasurement.normalizedMeasurements:
                return None
            for normalizedMeasurement in self.normalizedframeMeasurement.normalizedMeasurements:
                if normalizedMeasurement.landmark == NormalizedLandmarkPosition.HEEL:
                    heelMeasurement = normalizedMeasurement
                    break
            if heelMeasurement is None:
                return None

            # Raise error if one of the measurements is missing
            if footIndexMeasurement is None or heelMeasurement is None:
                raise EmptyDataException("Not enough data to calculate right foot angle")
            footAngle = self.operation.calculateAngleWithXAxis(
                (footIndexMeasurement.x, footIndexMeasurement.y),
                (heelMeasurement.x, heelMeasurement.y)
            )
            return round(footAngle, 2)
        except AttributeError:
            return None

