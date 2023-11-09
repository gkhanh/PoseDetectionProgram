class SquatRepCounter:
    def __init__(self, measurements):
        self.measurements = measurements
        self.windowSizeMillis = 1000
        self.getMeasurementsInWindow = []
        self.lowestPointList = []
        self.minimaIndices = []  # Array stores the position of data point that has the lowest point data

    def count(self):
        # List of landmarks that are recognized as a squat
        repetitions = []
        for i in range(1, len(self.measurements)):

            # getLandmarksInWindow will return a list of measurements in the window
            # It goes back in time for the length of the windowSizeMillis
            window = self.getMeasurementsInWindow[i - self.windowSizeMillis:i]

            print(window)

            # # TODO tune this number
            # if len(window) < 10:
            #     continue
            #
            # # Returns a landmark that is recognizes as a squat
            # repetitionInWindow = self.findRepetition(window)
            #
            # if repetitionInWindow is not None:
            #     # isAllowed will check if the repetition is not too close to any other squat
            #     if self.isNotTooCloseToOtherRepetition(repetitionInWindow, repetitions):
            #         repetitions.append(repetitionInWindow)
