import csv

import matplotlib.pyplot as plt


class CSVProcessor:
    def __init__(self, csvFile='D:/MoveLabStudio/Assignment/PoseDetectionPrototype/output/output.csv'):
        self.csvFile = csvFile
        self.x1 = []
        self.x2 = []
        self.y1 = []
        self.y2 = []
        self.windowStart = 0
        self.windowWidth = 10
        self.validRep = []
        self.lowestPointList = []
        self.minimaIndices = [] # Array stores the position of data point that has the lowest point data

    def processCSVFile(self):
        with open(self.csvFile, 'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            for row in lines:
                if row[1] == "RIGHT_HIP":
                    self.x1.append(row[0])
                    self.y1.append(float(row[3]))
                if row[1] == "RIGHT_KNEE":
                    self.x2.append(row[0])
                    self.y2.append(float(row[3]))

    def lowestPointInWindow(self):
        for self.windowStart in range(0, len(self.y2), self.windowWidth):
            # Determine the end of the window
            windowEnd = min(self.windowStart + self.windowWidth, len(self.y2))
            # Extract the window data
            windowY = self.y2[self.windowStart:windowEnd]
            lowestPoint = min(windowY)
            self.lowestPointList.append(lowestPoint)
        print(self.lowestPointList)

    def EligibleLowestPoint(self):
        for i in range(self.windowWidth, len(self.y2) - self.windowWidth):
            # If the current point is less than all points in the window around it
            if self.y2[i] == min(self.y2[i - self.windowWidth:i + self.windowWidth]):
                self.minimaIndices.append(i)
        print(self.minimaIndices)
        return len(self.minimaIndices)

    def displayResult(self):
        ax1 = plt.axes()
        ax1.set_xticklabels([])
        plt.plot(self.x1, self.y1, color='g', linewidth=0.2)
        plt.plot(self.x1, self.y2, color='r', linewidth=0.2)
        for i in range(len(self.minimaIndices)):
            x = self.minimaIndices[i]
            y = self.lowestPointList[i]
            plt.vlines(x, 0, y, colors='b', linewidth=0.2)  # Draw lines to x-axis
        plt.xticks(rotation=90)
        plt.xlabel('Amplitude')
        plt.ylabel('Time')
        plt.title('Sample Data', fontsize=20)
        plt.show()


def main():
    processor = CSVProcessor()
    processor.processCSVFile()
    processor.lowestPointInWindow()
    processor.EligibleLowestPoint()
    processor.displayResult()


if __name__ == "__main__":
    main()
