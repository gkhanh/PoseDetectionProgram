import csv


class CSVWriter:
    def __init__(self, outputCSV):
        csvfile = open(outputCSV, 'w', newline='')
        self.counter = 0
        self.csvWriter = csv.writer(csvfile)

    @staticmethod
    def writeFrameMeasurement(frameMeasurements):
        if len(frameMeasurements) == 0:
            print("No data to write")

    def writeRow(self, row: list):
        self.csvWriter.writerow(row)

    def addLine(self, line):
        # Limit the data written to csv to 10000 lines
        while self.counter < 10000:
            for _ in range(10000):
                self.writeRow(line)
                self.counter += 1
                if self.counter >= 10000:
                    break
                return line
            if self.counter >= 10000:
                break
        return line

