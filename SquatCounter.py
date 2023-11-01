import CSVWriter
import PoseModule


class RepCounter:

    def __init__(self):
        self.repetitions = 0
        self.currentHipWindow = []
        self.currentKneeWindow = []

    def offerMeasurement(self, measurement):
        (frameNumber, landmark, x, y, z) = measurement
        if landmark not in ["RIGHT_HIP", "RIGHT_KNEE"]:
            # Ignore any measurements not for the hip or knee
            return

        # At this point we only have data form the right hip and right knee
        if landmark == "RIGHT_HIP":
            self.currentHipWindow.append(measurement.y)
            if len(self.currentHipWindow) > 90:
                self.currentHipWindow.pop(0)

        if landmark == "RIGHT_KNEE":
            self.currentKneeWindow.append(measurement.y)
            if len(self.currentKneeWindow) > 90:
                self.currentKneeWindow.pop(0)

        self.detectRepetition()

    def detectRepetition(self):
        if len(self.currentHipWindow) < 90:
            # Ignore any startup
            return
        avgKneeValue = sum(self.currentKneeWindow) / len(self.currentKneeWindow)
        avgHipValue = sum(self.currentHipWindow) / len(self.currentHipWindow)

        # Define a threshold for squat detection
        threshold = avgKneeValue - (avgKneeValue - avgHipValue)

        minValue = min(self.currentHipWindow)
        pass
        if minValue < threshold:
            # Ensure that you are not counting the same repetition multiple times
            if len(self.currentHipWindow) >= 90:
                if minValue == self.currentHipWindow[45]:
                    # Increment the repetition count
                    self.repetitions += 1
                    # Remove processed data to avoid counting the same repetition again
                    self.currentHipWindow = self.currentHipWindow[45:]
        return self.repetitions

# def main():
#     # Create a sorted and filtered CSV file
#     dataStream = pd.read_csv('output/output.csv')
#     # Initialize the RepCounter
#     repCounter = RepCounter()
#     for index, row in dataStream.iterrows():
#         repCounter.offerMeasurement(row)
#     # Print the total number of repetitions detected
#     print("Total Repetitions:", repCounter.repetitions)
#
#
# if __name__ == "__main__":
#     main()
