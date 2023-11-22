from src.utils.MathUtils import MathUtils
from src.models.measurement import LandmarkPosition
from src.exception.EmptyDataException import EmptyDataException


class CalculatedAngles:
    def __init__(self, frameMeasurement) -> None:
        self.frameMeasurement = frameMeasurement
        self.operation = MathUtils()

    def calculateRightHipAngle(self):
        try:
            # Find the RIGHT_KNEE
            rightKneeMeasurement = None
            if not self.frameMeasurement.measurements:
                print("Empty data")
                return None
            for measurement in self.frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.RIGHT_KNEE:
                    rightKneeMeasurement = measurement
                    break
            if rightKneeMeasurement is None:
                return None

            # Find the RIGHT_HIP
            rightHipMeasurement = None
            if not self.frameMeasurement.measurements:
                print("Empty data")
                return None
            for measurement in self.frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.RIGHT_HIP:
                    rightHipMeasurement = measurement
                    break
            if rightHipMeasurement is None:
                return None

            # Find the RIGHT_SHOULDER
            rightShoulderMeasurement = None
            if not self.frameMeasurement.measurements:
                print("Empty data")
                return None
            for measurement in self.frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.RIGHT_SHOULDER:
                    rightShoulderMeasurement = measurement
                    break
            if rightShoulderMeasurement is None:
                return None

            # Raise error if one of the measurements is missing
            if rightKneeMeasurement is None or rightHipMeasurement is None or rightShoulderMeasurement is None:
                raise EmptyDataException("Not enough data to calculate right hip angle")

            rightHipAngle = self.operation.calculateAngle(
                (rightShoulderMeasurement.x, rightShoulderMeasurement.y),
                (rightHipMeasurement.x, rightHipMeasurement.y),
                (rightKneeMeasurement.x, rightKneeMeasurement.y),
            )
            return round(rightHipAngle, 2)
        except AttributeError:
            return None

    def calculateRightKneeAngle(self):
        try:
            # Find the RIGHT_KNEE
            rightKneeMeasurement = None
            if not self.frameMeasurement.measurements:
                print("Empty data")
                return None
            for measurement in self.frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.RIGHT_KNEE:
                    rightKneeMeasurement = measurement
                    break
            if rightKneeMeasurement is None:
                return None

            # Find the RIGHT_ANKLE
            rightAnkleMeasurement = None
            if not self.frameMeasurement.measurements:
                print("Empty data")
                return None
            for measurement in self.frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.RIGHT_ANKLE:
                    rightAnkleMeasurement = measurement
                    break
            if rightAnkleMeasurement is None:
                return None

            # Find the RIGHT_HIP
            rightHipMeasurement = None
            if not self.frameMeasurement.measurements:
                print("Empty data")
                return None
            for measurement in self.frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.RIGHT_HIP:
                    rightHipMeasurement = measurement
                    break
            if rightHipMeasurement is None:
                return None

            # Raise error if one of the measurements is missing
            if rightKneeMeasurement is None or rightHipMeasurement is None or rightAnkleMeasurement is None:
                raise EmptyDataException("Not enough data to calculate knee angle")

            rightKneeAngle = self.operation.calculateAngle(
                (rightHipMeasurement.x, rightHipMeasurement.y),
                (rightKneeMeasurement.x, rightKneeMeasurement.y),
                (rightAnkleMeasurement.x, rightAnkleMeasurement.y),
            )
            return round(rightKneeAngle, 2)

        except AttributeError:
            return None

    def calculateRightShoulderAngle(self):
        try:
            # Find the RIGHT_SHOULDER
            rightShoulderMeasurement = None
            if not self.frameMeasurement.measurements:
                print("Empty data")
                return None
            for measurement in self.frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.RIGHT_SHOULDER:
                    rightShoulderMeasurement = measurement
                    break
            if rightShoulderMeasurement is None:
                return None

            # Find the RIGHT_ELBOW
            rightElbowMeasurement = None
            if not self.frameMeasurement.measurements:
                print("Empty data")
                return None
            for measurement in self.frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.RIGHT_ELBOW:
                    rightElbowMeasurement = measurement
                    break
            if rightElbowMeasurement is None:
                return None

            # Find the RIGHT_HIP
            rightHipMeasurement = None
            if not self.frameMeasurement.measurements:
                print("Empty data")
                return None
            for measurement in self.frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.RIGHT_HIP:
                    rightHipMeasurement = measurement
                    break
            if rightHipMeasurement is None:
                return None

            # Raise error if one of the measurements is missing
            if rightShoulderMeasurement is None or rightElbowMeasurement is None or rightHipMeasurement is None:
                raise EmptyDataException("Not enough data to calculate right shoulder angle")

            shoulderAngle = self.operation.calculateAngle(
                (rightHipMeasurement.x, rightHipMeasurement.y),
                (rightShoulderMeasurement.x, rightShoulderMeasurement.y),
                (rightElbowMeasurement.x, rightElbowMeasurement.y),
            )
            return round(shoulderAngle, 2)
        except AttributeError:
            return None

    def calculateRightElbowAngle(self):
        try:
            # Find the RIGHT_SHOULDER
            rightShoulderMeasurement = None
            if not self.frameMeasurement.measurements:
                print("Empty data")
                return None
            for measurement in self.frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.RIGHT_SHOULDER:
                    rightShoulderMeasurement = measurement
                    break
            if rightShoulderMeasurement is None:
                return None

            # Find the RIGHT_ELBOW
            rightElbowMeasurement = None
            if not self.frameMeasurement.measurements:
                print("Empty data")
                return None
            for measurement in self.frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.RIGHT_ELBOW:
                    rightElbowMeasurement = measurement
                    break
            if rightElbowMeasurement is None:
                return None

            # Find the RIGHT_WRIST
            rightWristMeasurement = None
            if not self.frameMeasurement.measurements:
                print("Empty data")
                return None
            for measurement in self.frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.RIGHT_WRIST:
                    rightWristMeasurement = measurement
                    break
            if rightWristMeasurement is None:
                return None

            # Raise error if one of the measurements is missing
            if rightShoulderMeasurement is None or rightElbowMeasurement is None or rightWristMeasurement is None:
                raise EmptyDataException("Not enough data to calculate right elbow angle")

            elbowAngle = self.operation.calculateAngle(
                (rightShoulderMeasurement.x, rightShoulderMeasurement.y),
                (rightElbowMeasurement.x, rightElbowMeasurement.y),
                (rightWristMeasurement.x, rightWristMeasurement.y),
            )
            return round(elbowAngle, 2)
        except AttributeError:
            return None
    def calculateLeftKneeAngle(self):
        try:
            # Find the LEFT_KNEE
            leftKneeMeasurement = None
            if not self.frameMeasurement.measurements:
                return None
            for measurement in self.frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.LEFT_KNEE:
                    leftKneeMeasurement = measurement
                    break
            if leftKneeMeasurement is None:
                return None

            # Find the LEFT_ANKLE
            leftAnkleMeasurement = None
            if not self.frameMeasurement.measurements:
                return None
            for measurement in self.frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.LEFT_ANKLE:
                    leftAnkleMeasurement = measurement
                    break
            if leftAnkleMeasurement is None:
                return None

            # Find the LEFT_HIP
            leftHipMeasurement = None
            if not self.frameMeasurement.measurements:
                return None
            for measurement in self.frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.LEFT_HIP:
                    leftHipMeasurement = measurement
                    break
            if leftHipMeasurement is None:
                return None

            # Raise error if one of the measurements is missing
            if leftKneeMeasurement is None or leftHipMeasurement is None or leftAnkleMeasurement is None:
                raise EmptyDataException("Not enough data to calculate knee angle")

            rightKneeAngle = self.operation.calculateAngle(
                (leftHipMeasurement.x, leftHipMeasurement.y),
                (leftKneeMeasurement.x, leftKneeMeasurement.y),
                (leftAnkleMeasurement.x, leftAnkleMeasurement.y),
            )
            return round(rightKneeAngle, 2)
        except AttributeError:
            return None




