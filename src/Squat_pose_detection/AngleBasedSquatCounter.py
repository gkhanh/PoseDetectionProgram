from src.models.Measurement import LandmarkPosition
from src.utils.CalculatedAngles import CalculatedAngles
from src.utils.Cancellable import Cancellable


# New strategy that uses only angles
class AngleBasedSquatCounter:

    def __init__(self) -> None:
        self.squatAngles = []
        self.stage = None
        self.counter = 0
        self.lastRightHipAngles = []
        self.lastRightKneeAngles = []
        self.lastLeftHipAngles = []
        self.lastLeftKneeAngles = []

        self.listeners = []

    def addListener(self, listener):
        self.listeners.append(listener)

        return Cancellable(lambda: self.listeners.remove(listener))

    def onMeasurement(self, frameMeasurement):
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

    def isProperSquat(self, frameMeasurement):
        angleCalculator = CalculatedAngles(frameMeasurement)
        angles = self.getCalculatedAngles(angleCalculator)
        if any(angle is None for angle in angles):
            self.resetAngles()
            return
        self.appendAngles(angles)
        self.checkAngleLists()
        self.checkSquatStage(frameMeasurement)

    def getCalculatedAngles(self, angleCalculator):
        rightHipAngle = angleCalculator.calculateRightHipAngle()
        rightKneeAngle = angleCalculator.calculateRightKneeAngle()
        leftHipAngle = angleCalculator.calculateLeftHipAngle()
        leftKneeAngle = angleCalculator.calculateLeftKneeAngle()
        return rightKneeAngle, rightHipAngle, leftKneeAngle, leftHipAngle

    def resetAngles(self):
        # print("Knee angle is None or hip angle is None")
        self.lastRightKneeAngles = []
        self.lastRightHipAngles = []
        self.lastLeftKneeAngles = []
        self.lastLeftHipAngles = []

    def appendAngles(self, angles):
        self.lastRightHipAngles.append(angles[1])
        self.lastRightKneeAngles.append(angles[0])
        self.lastLeftHipAngles.append(angles[3])
        self.lastLeftKneeAngles.append(angles[2])

    def checkAngleLists(self):
        for angleList in [self.lastRightKneeAngles, self.lastRightHipAngles, self.lastLeftKneeAngles,
                          self.lastLeftHipAngles]:
            if len(angleList) > 5:
                angleList.pop(0)
            if len(angleList) < 5:
                return

    def checkSquatStage(self, frameMeasurement):
        # For right side
        self.checkSideSquatStage(self.lastRightKneeAngles, self.lastRightHipAngles, frameMeasurement)
        # For left side
        self.checkSideSquatStage(self.lastLeftKneeAngles, self.lastLeftHipAngles, frameMeasurement)

    def checkSideSquatStage(self, kneeAngles, hipAngles, frameMeasurement):
        if all(angle <= 70 for angle in kneeAngles) and all(angle <= 70 for angle in hipAngles):
            if self.stage != "down" and self.compareXCoordinateKneeAndFoot(frameMeasurement):
                print(f'squat count: {self.counter}; stage: down;')
                self.notifyListeners()
                self.stage = "down"
                self.counter += 1

        if all(angle >= 150 for angle in kneeAngles) and all(
                angle >= 150 for angle in hipAngles) and self.stage != "up":
            print('stage: up;')
            self.stage = "up"

    def compareXCoordinateKneeAndFoot(self, frameMeasurement):
        rightKneeXCoordinate = None
        rightFootXCoordinate = None
        leftKneeXCoordinate = None
        leftFootXCoordinate = None
        for measurement in frameMeasurement.measurements:
            if measurement.landmark == LandmarkPosition.RIGHT_KNEE:
                rightKneeXCoordinate = measurement.x
            if measurement.landmark == LandmarkPosition.RIGHT_FOOT_INDEX:
                rightFootXCoordinate = measurement.x
                break
            if measurement.landmark == LandmarkPosition.LEFT_KNEE:
                leftKneeXCoordinate = measurement.x
            if measurement.landmark == LandmarkPosition.LEFT_FOOT_INDEX:
                leftFootXCoordinate = measurement.x
                break

        def isWithinRange(coordinate1, coordinate2):
            return coordinate1 is not None and coordinate2 is not None and coordinate1 - 0.19 < coordinate2 < coordinate1 + 0.19

        if isWithinRange(leftKneeXCoordinate, leftFootXCoordinate) or isWithinRange(rightKneeXCoordinate,
                                                                                    rightFootXCoordinate):
            print("Squat detected")
            return True
        else:
            print("Knee or foot not detected")
            return False

    def notifyListeners(self):
        for listener in self.listeners:
            listener.onSquat(self.counter)

    class Listener:
        def onSquat(self, counter):
            raise NotImplementedError
