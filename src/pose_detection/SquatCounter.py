from src.utils.plotDataFromCSV import CSVProcessor


class SquatRepCounter:
    def __init__(self):
        self.repetitions = 0
        self.windowStart = 0
        self.windowWidth = 10
        self.kneeData = []
        self.hipData = []
        self.lowestPointList = []
        self.minimaIndices = []  # Array stores the position of data point that has the lowest point data

    def detectSquatBasedOnLowestPoint(self, data: CSVProcessor):
        self.kneeData = data.getRightKneeData()
        self.hipData = data.getRightHipData()
        for self.windowStart in range(0, len(self.kneeData), self.windowWidth):
            # Determine the end of the window
            windowEnd = min(self.windowStart + self.windowWidth, len(self.kneeData))
            # Extract the window data
            windowY = self.kneeData[self.windowStart:windowEnd]
            lowestPoint = min(windowY)
            self.lowestPointList.append(lowestPoint)

    def countRepetitions(self, data: CSVProcessor):
        self.kneeData = data.getRightKneeData()
        self.hipData = data.getRightHipData()
        for i in range(self.windowWidth, len(self.kneeData) - self.windowWidth):
            # If the current point is less than all points in the window around it
            if self.kneeData[i] == min(self.kneeData[i - self.windowWidth:i + self.windowWidth]):
                self.minimaIndices.append(i)
        for j in range(len(self.minimaIndices)-1, 0, -1):
            if self.minimaIndices[j] - self.minimaIndices[j-1] <= self.windowWidth:
                self.minimaIndices.pop(j)
        self.repetitions = len(self.minimaIndices)
        return self.repetitions

