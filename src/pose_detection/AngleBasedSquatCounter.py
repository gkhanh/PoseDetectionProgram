from src.utils.CalculatedAngles import CalculatedAngles


# New strategy that uses only angles
class AngleBasedSquatCounter:
    def __init__(self) -> None:
        self.squatAngles = []
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
        self.squatAngles.append(rightHipAngle)
        self.squatAngles.append(rightKneeAngle)
        self.squatAngles.append(rightShoulderAngle)
        self.squatAngles.append(rightElbowAngle)
        print(self.squatAngles)
        return self.squatAngles

    def isProperSquat(self, frameMeasurement):
        angleCalculator = CalculatedAngles(frameMeasurement)
        rightHipAngle = angleCalculator.calculateRightHipAngle()
        rightKneeAngle = angleCalculator.calculateRightKneeAngle()
        rightShoulderAngle = angleCalculator.calculateRightShoulderAngle()
        rightElbowAngle = angleCalculator.calculateRightElbowAngle()
        if rightKneeAngle > 150:
            if self.stage != "up":
                self.stage = "up"
                print(f'squat count: {self.counter}; stage: {self.stage};')
        if rightKneeAngle <= 90 and self.stage == 'up':
            self.stage = "down"
            self.counter += 1
            print(f'squat count: {self.counter}; stage: {self.stage};')