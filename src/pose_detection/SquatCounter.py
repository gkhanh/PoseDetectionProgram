from typing import Optional

from src.models.measurement import LandmarkPosition
from src.pose_detection.PoseDetector import Measurement
from src.utils.MathUtils import calculate_angle


class SquatRepCounter:
    def __init__(self):
        self.measurements = []
        self.windowStart = 0
        self.windowSizeMillis = 1000.0
        self.getMeasurementsInWindow = []
        self.kneeData = []
        self.hipData = []

        self.repetitions = []

    def offerMeasurement(self, measurement: Measurement):
        self.measurements.append(measurement)

        # Pop measurements when they are outside the windowSizeMillis
        while self.measurements[0].timestamp < measurement.timestamp - self.windowSizeMillis:
            self.measurements.pop(0)

        self.updateRepetitions()

    def updateRepetitions(self):
        # Filter only RIGHT_KNEE
        measurements = [measurement for measurement in self.measurements if
                        measurement.landmark == LandmarkPosition.RIGHT_HIP]

        for measurement in measurements:
            window = self.getWindowForMeasurement(measurement, measurements)

            if len(window) < 10:
                continue

            # Returns a landmark that is recognized as a squat
            repetitionInWindow = self.findRepetition(window)
            if repetitionInWindow is not None:
                # isAllowed will check if the repetition is not too close to any other squat
                if self.isNotTooCloseToOtherRepetition(repetitionInWindow, self.repetitions):
                    self.repetitions.append(repetitionInWindow)
                    print("Repetition detected at " + str(repetitionInWindow.timestamp) + "ms")
            self.curlCounterLogic()

    def getWindowForMeasurement(self, currentMeasurement, measurements):
        window = []

        # Look back in time to find the first measurement that is within the window
        startTimeOfWindow = currentMeasurement.timestamp - self.windowSizeMillis
        endTimeOfWindow = currentMeasurement.timestamp

        # Loop in reverse till we're outside the window
        for measurement in reversed(measurements):
            if startTimeOfWindow <= measurement.timestamp <= endTimeOfWindow:
                window.append(measurement)

        return window

    def findRepetition(self, window) -> Optional[Measurement]:
        yCoordinates = [measurement.y for measurement in window]

        lowestPointIndex = yCoordinates.index(min(yCoordinates))

        # If we're going up or down it's not a local low
        if lowestPointIndex == 0 or lowestPointIndex == len(window) - 1:
            return None

        return window[lowestPointIndex]

    # function to check if the repetition is not too close to any other repetition
    def isNotTooCloseToOtherRepetition(self, repetitionToConsider, repetitions):
        for i in range(len(repetitions)):
            # If the current point is less than all points in the window around it
            if abs(repetitionToConsider.timestamp - repetitions[i].timestamp) < self.windowSizeMillis:
                return False
        return True

    def curlCounterLogic(self):
        # angle = calculate_angle(shoulder, elbow, wrist)
        angleMin = []
        angleMinHip = []
        # rightHipList = [measurement.x, measurement.y for measurement in self.measurements if measurement.landmark == LandmarkPosition.RIGHT_HIP]
        # rightKneeList = [measurement.x, measurement.y for measurement in self.measurements if measurement.landmark == LandmarkPosition.RIGHT_KNEE]
        # rightShoulderList = [measurement.x, measurement.y for measurement in self.measurements if measurement.landmark == LandmarkPosition.RIGHT_SHOULDER]
        # rightAnkleList = [measurement.x, measurement.y for measurement in self.measurements if measurement.landmark == LandmarkPosition.RIGHT_ANKLE]

        rightHipList = [[measurement.x, measurement.y] for measurement in self.measurements if
                        measurement.landmark == LandmarkPosition.RIGHT_HIP][0]
        rightKneeList = [[measurement.x, measurement.y] for measurement in self.measurements if
                         measurement.landmark == LandmarkPosition.RIGHT_KNEE][0]
        rightShoulderList = [[measurement.x, measurement.y] for measurement in self.measurements if
                             measurement.landmark == LandmarkPosition.RIGHT_SHOULDER][0]
        rightAnkleList = [[measurement.x, measurement.y] for measurement in self.measurements if
                          measurement.landmark == LandmarkPosition.RIGHT_ANKLE][0]

        angleKnee = calculate_angle(rightHipList, rightKneeList, rightAnkleList)  # Knee joint angle
        angleKnee = round(angleKnee, 2)

        angleHip = calculate_angle(rightShoulderList, rightHipList, rightKneeList)
        angleHip = round(angleHip, 2)

        hipAngle = 180 - angleHip
        kneeAngle = 180 - angleKnee

        angleMin.append(angleKnee)
        angleMinHip.append(angleHip)

        # print(angleKnee)
        if angleKnee > 150:
            stage = "up"
        if angleKnee <= 90: # and stage == 'up':
            stage = "down"
            counter = 0
            counter += 1
            print(counter)
            min_ang = min(angleMin)
            max_ang = max(angleMin)

            min_ang_hip = min(angleMinHip)
            max_ang_hip = max(angleMinHip)

            # print(min(angleMin), " _ ", max(angleMin))
            # print(min(angleMinHip), " _ ", max(angleMinHip))
            angleMin = []
            angleMinHip = []
