import mediapipe as mp
from src.utils.plotDataFromCSV import CSVProcessor


class SquatRepCounter:
    def __init__(self):
        self.repetitions = 0
        self.currentHipWindow = []
        self.currentKneeWindow = []

        self.windowWidth = 60
        self.rep = []
        self.legitSquatTime = 30
        self.lastSquatTime = -self.legitSquatTime  # Initialize to a value that allows the first squat to be counted

    def offerMeasurement(self, measurement):
        [_, landmark, _, y, _] = measurement
        measuringBodyPart = ["RIGHT_HIP", "RIGHT_KNEE"]
        if landmark not in measuringBodyPart:
            # Ignore any measurements not for the hip or knee
            return

        # At this point we only have data form the right hip and right knee
        if landmark == "RIGHT_HIP":
            self.currentHipWindow.append(y)
            if len(self.currentHipWindow) > self.windowWidth:
                self.currentHipWindow.pop(0)

        if landmark == "RIGHT_KNEE":
            self.currentKneeWindow.append(y)
            if len(self.currentKneeWindow) > self.windowWidth:
                self.currentKneeWindow.pop(0)

        self.detectRepetition()

    def detectRepetition(self):
        if len(self.currentHipWindow) < self.windowWidth:
            # Not enough data yet
            return

        for i in range(self.windowWidth, -1, -1):
            self.currentHipWindow = self.currentHipWindow[i:]
            minHipWindow = min(self.currentHipWindow)
            print("number:", minHipWindow)



