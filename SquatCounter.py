class SquatRepCounter:
    def __init__(self):
        self.repetitions = 0
        self.currentHipWindow = []
        self.currentKneeWindow = []

    def offerMeasurement(self, measurement):
        [frameNumber, landmark, x, y, z] = measurement
        if landmark not in ["RIGHT_HIP", "RIGHT_KNEE"]:
            # Ignore any measurements not for the hip or knee
            return

        # At this point we only have data form the right hip and right knee
        if landmark == "RIGHT_HIP":
            self.currentHipWindow.append(y)
            if len(self.currentHipWindow) > 90:
                self.currentHipWindow.pop(0)

        if landmark == "RIGHT_KNEE":
            self.currentKneeWindow.append(y)
            if len(self.currentKneeWindow) > 90:
                self.currentKneeWindow.pop(0)

        if self.detectRepetition():
            self.repetitions += 1
            print("Total Repetitions:", self.repetitions)

    def detectRepetition(self):
        if len(self.currentHipWindow) < 90:
            # Ignore any startup
            return False
        avgKneeValue = round(sum(self.currentKneeWindow) / len(self.currentKneeWindow), 3)
        avgHipValue = round(sum(self.currentHipWindow) / len(self.currentHipWindow), 3)
        # Define a threshold for squat detection
        threshold = avgKneeValue - (avgKneeValue - avgHipValue)
        currentHipValue = self.currentHipWindow[-1]
        if currentHipValue < min(self.currentHipWindow[:-1]) and currentHipValue < threshold:
            return True
        return False
    # def offerMeasurement(self, measurement):
    #     [frameNumber, landmark, x, y, z] = measurement
    #     if landmark not in ["RIGHT_HIP", "RIGHT_KNEE"]:
    #         # Ignore any measurements not for the hip or knee
    #         return
    #     else:
    #         if landmark == "RIGHT_HIP":
    #             self.currentHipWindow.append(y)
    #             if len(self.currentHipWindow) > 100:
    #                 self.currentHipWindow.pop(0)
    #
    #         if landmark == "RIGHT_KNEE":
    #             self.currentKneeWindow.append(y)
    #             if len(self.currentKneeWindow) > 100:
    #                 self.currentKneeWindow.pop(0)
    #
    #         if landmark == "RIGHT_HIP":
    #             self.hipValue = y
    #         if landmark == "RIGHT_KNEE":
    #             self.kneeValue = y
    #
    #         self.detectRepetition()
    #
    # def detectRepetition(self):
    #     # calculate threshold value
    #     avg_diff = np.mean([abs(self.hipValue - self.kneeValue) for self.hipValue, self.kneeValue in
    #                         zip(self.currentHipWindow, self.currentKneeWindow)])
    #     if self.state == "stand":
    #         if self.hipValue <= float(self.kneeValue) + avg_diff:
    #             self.state = "squat"
    #     elif self.state == "squat":
    #         if self.hipValue > float(self.kneeValue) + avg_diff:
    #             self.state = "stand"
    #             self.repetitions += 1
    #             print("Total Repetitions:", self.repetitions)
