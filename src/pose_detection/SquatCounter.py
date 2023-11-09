from typing import Optional
from src.entity.Measurement import Measurement


class SquatRepCounter:
    def __init__(self, measurements):
        self.measurements = measurements
        self.windowSizeMillis = 1000
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

    # TODO fix this function
    def count(self):
        # List of landmarks that are recognized as a squat
        repetitions = []

        for i in range(0, len(self.measurements)):
            # getLandmarksInWindow will return a list of measurements in the window
            # It goes back in time for the length of the windowSizeMillis
            window = self.getMeasurementsInWindow[i - self.windowSizeMillis:i]
            print(window)

            if len(window) < 10:
                continue

            # Returns a landmark that is recognizes as a squat
            repetitionInWindow = self.findRepetition()

            if repetitionInWindow is not None:
                # isAllowed will check if the repetition is not too close to any other squat
                if self.isNotTooCloseToOtherRepetition(repetitionInWindow, repetitions):
                    repetitions.append(repetitionInWindow)
        return len(repetitions)

    def findRepetition(self, window) -> Optional[Measurement]:
        repetition = Measurement(0, '', 0, 0, 0)
        #TODO fix the range of for loop
        for i in range(window):
            # If the current point is less than all points in the window around it
            #TODO fix the condition
            if self.kneeData[i] == min(self.kneeData[i - self.windowSizeMillis:i + self.windowSizeMillis]):
                # repetition = self.measurements[self.kneeData[i]]
                #TODO assign the matched measurement into repetition
                repetition = [measurement for measurement in self.measurements if measurement.y == self.kneeData[i]]
                # print(repetition)
        return repetition

    # function to check if the repetition is not too close to any other repetition
    #TODO test and fix this function
    def isNotTooCloseToOtherRepetition(self, repetitionInWindow, repetitions):
        for i in range(len(repetitions)):
            # return false if the timestamp of the current repetition minus the previous repetition timestamp
            # is less than windowSize
            # or a repetition is found inside the window that contains the current repetition
            if abs(repetitions[i - 1].timestamp - repetitions[i].timestamp) < self.windowSizeMillis or repetitionInWindow == repetitions[i]:
                return False
        return True
