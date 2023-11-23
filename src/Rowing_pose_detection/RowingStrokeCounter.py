from src.utils.CalculatedAngles import CalculatedAngles


class RowingExerciseCounter:
    def __init__(self) -> None:
        self.bodyAngles = []
        self.stage = None
        self.counter = 0

    def offerMeasurement(self, frameMeasurement) -> list:
        # Filter only RIGHT_KNEE
        angleCalculator = CalculatedAngles(frameMeasurement)
        # calculate hip angle
        rightHipAngle = angleCalculator.calculateRightHipAngle()
        rightKneeAngle = angleCalculator.calculateRightKneeAngle()
        rightShoulderAngle = angleCalculator.calculateRightShoulderAngle()
        rightElbowAngle = angleCalculator.calculateRightElbowAngle()
        self.bodyAngles.append(rightHipAngle)
        self.bodyAngles.append(rightKneeAngle)
        self.bodyAngles.append(rightShoulderAngle)
        self.bodyAngles.append(rightElbowAngle)
        print(self.bodyAngles)
        return self.bodyAngles

    def isRecoveryPhase(self):

        return True

    def isDrivePhase(self):
        return True

    def isProperRowingRecoveryStroke(self):
        pass

    def isProperRowingDriveExercise(self):
        pass