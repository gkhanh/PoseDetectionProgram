from src.utils.CalculatedAngles import CalculatedAngles


# New strategy that uses only angles
class AngleBasedSquatCounter:
    def __init__(self) -> None:
        self.squatAngles = []
        self.stage = None
        self.counter = 0
        self.lastRightKneeAngles = []

    def offerMeasurement(self, frameMeasurement):
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

    def isProperSquat(self, frameMeasurement):
        angleCalculator = CalculatedAngles(frameMeasurement)
        rightHipAngle = angleCalculator.calculateRightHipAngle()
        rightKneeAngle = angleCalculator.calculateRightKneeAngle()
        rightShoulderAngle = angleCalculator.calculateRightShoulderAngle()
        rightElbowAngle = angleCalculator.calculateRightElbowAngle()

        if rightKneeAngle is None:
            print("Knee angle is None")
            self.lastRightKneeAngles = []
            return

        self.lastRightKneeAngles.append(rightKneeAngle)

        # Limit the last 5 angles
        if len(self.lastRightKneeAngles) > 5:
            self.lastRightKneeAngles.pop(0)

        # We want at least 5 measurements
        if len(self.lastRightKneeAngles) < 5:
            return

        if all(angle <= 90 for angle in self.lastRightKneeAngles):
            # We're now in a squat position
            if self.stage != "down":
                print(f'squat count: {self.counter}; stage: down;')
                self.stage = "down"
                self.counter += 1

        if all(angle >= 150 for angle in self.lastRightKneeAngles):
            # We're now in a standing position
            if self.stage != "up":
                print('stage: up;')
                self.stage = "up"

