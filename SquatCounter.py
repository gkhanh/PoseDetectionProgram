import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm

class RepCounter:

    def __init__(self):
        self.repetitions = 0

        self.currentHipWindow = []
        self.currentKneeWindow = []

    def offerMeasurement(self, measurement):
        (frame_number, landmark, x, y, z) = measurement

        if landmark not in ["RIGHT_HIP", "RIGHT_KNEE"]:
            return

        # At this point we only have data form the right hip and right knee
        if landmark == "RIGHT_HIP":
            self.previousHipLocations.append((x, y, z))
            # Select 3 seconds of data
            # TODO make sure we're not using frame number but time
            if len(self.previousHipLocations) > 90:
                self.previousHipLocations.pop(0)

        if landmark == "RIGHT_KNEE":
            self.previousKneeLocations.append((x, y, z))
            # Prevent list from growing too large
            if len(self.previousKneeLocations) > 10:
                self.previousKneeLocations.pop(0)

        self.detectRepetition()

    def detectRepetition(self):
        # TODO implement algorithm to see if last added measurement create a repition

        localMinimum = self.findLocalMinimum(self.currentHipWindow)
        if self.meetsSquatRequirement(localMinimum, this.currentKneeWindow):
            self.repetitions += 1



# Create a sorted and filtered csv file
dataStream = pd.read_csv('output/output.csv', index_col="landmark")

# Loop over each line
repCounter = RepCounter()

for index, row in dataStream.iterrows():
    repCounter.offerMeasurement(row)