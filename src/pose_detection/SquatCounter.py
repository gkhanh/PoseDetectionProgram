from typing import Optional

from src.entity.Measurement import Measurement


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
            if measurement.landmark == "RIGHT_HIP":
                self.hipData.append(measurement.y)
            elif measurement.landmark == "RIGHT_KNEE":
                self.kneeData.append(measurement.y)

    # def getAllMeasurementInWindow(self):
    #     pass

    def getAllMeasurementInWindowAndCount(self):
        # List of landmarks that are recognized as a squat
        repetitions = []
        windows = []    # list of windows
        window = []     # windows contains measurements with timestamps within 1000ms
        startTime = 0   # In milliseconds
        endTime = 1000.0    # In milliseconds

        for measurement in self.measurements:
            if startTime <= float(measurement.timestamp) <= endTime:
                window.append(measurement)
            else:
                if window:
                    windows.append(window)
                startTime = endTime + 1
                endTime = startTime + self.windowSizeMillis
                window = [measurement]

            # Returns a landmark that is recognized as a squat
            repetitionInWindow = self.findRepetition(window)
            if repetitionInWindow is not None:
                # isAllowed will check if the repetition is not too close to any other squat
                if self.isNotTooCloseToOtherRepetition(repetitions):
                    repetitions.append(repetitionInWindow)

        if window:
            windows.append(window)
        return len(repetitions)

    # def findRepetition(self, window) -> Optional[Measurement]:
    #     repetition = Measurement(0.0, '', 0, 0, 0)
    #     # TODO fix the range of for loop within the 'window' size
    #     for i in range(len(window)):
    #         # If the current point is less than all points in the window around it
    #         if window[i].y == min(measurement.y for measurement in window[max(0, i - int(self.windowSizeMillis)): min(
    #                 len(window), i + int(self.windowSizeMillis))]):
    #             # TODO assign the matched measurement into repetition
    #             repetition = window[i]
    #             # print(repetition)
    #     return repetition

    def findRepetition(self, window) -> Optional[Measurement]:
        repetition = Measurement(0.0, '', 0, 0, 0)
        lowestPoint = float('inf')
        # Find the lowest point based on y coordinate of measurement
        for measurement in window:
            if float(measurement.y) < lowestPoint:
                lowestPoint = float(measurement.y)
                repetition = measurement
        print(repetition)
        return repetition

    # function to check if the repetition is not too close to any other repetition
    def isNotTooCloseToOtherRepetition(self, repetitions):
        for i in range(len(repetitions)):
            # return false if the timestamp of the current repetition minus the previous repetition timestamp
            # is less than windowSize
            # or a repetition is found inside the window that contains the current repetition
            if abs(float(repetitions[i - 1].timestamp) - float(repetitions[i].timestamp)) < self.windowSizeMillis:
                return False
        return True
