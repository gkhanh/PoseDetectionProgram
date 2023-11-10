from typing import Optional

from src.models.measurement import LandmarkPosition
from src.pose_detection.PoseDetector import Measurement


class SquatRepCounter:
    def __init__(self, measurements):
        self.measurements = measurements
        self.windowStart = 0
        self.windowSizeMillis = 1000.0
        self.getMeasurementsInWindow = []
        self.kneeData = []
        self.hipData = []

    # Function to extract y coordinates of Measurement object to find repetitions
    def extractYCoordinateFromMeasurement(self):
        for measurement in self.measurements:
            if measurement.landmark == LandmarkPosition.RIGHT_HIP:
                self.hipData.append(measurement.y)
            elif measurement.landmark == LandmarkPosition.RIGHT_KNEE:
                self.kneeData.append(measurement.y)

    def getAllMeasurementInWindowAndCount(self):
        # List of landmarks that are recognized as a squat
        repetitions = []

        # Filter only RIGHT_KNEE
        measurements = [measurement for measurement in self.measurements if
                        measurement.landmark == LandmarkPosition.RIGHT_KNEE]

        for measurement in measurements:
            window = self.getWindowForMeasurement(measurement, measurements)

            if len(window) < 10:
                continue

            # Returns a landmark that is recognized as a squat
            repetitionInWindow = self.findRepetition(window)
            if repetitionInWindow is not None:
                # isAllowed will check if the repetition is not too close to any other squat
                if self.isNotTooCloseToOtherRepetition(repetitionInWindow, repetitions):
                    repetitions.append(repetitionInWindow)

        return len(repetitions)

    def getWindowForMeasurement(self, currentMeasurement, measurements):
        window = []

        # Look back in time to find the first measurement that is within the window
        startTimeOfWindow = currentMeasurement.timestamp - self.windowSizeMillis
        endTimeOfWindow = currentMeasurement.timestamp

        # Loop in reverse till we're outside of the window
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
