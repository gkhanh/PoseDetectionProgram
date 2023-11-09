import csv
from src.entity.Measurement import Measurement


class CSVWriter:
    def __init__(self, outputCSV):
        csvfile = open(outputCSV, 'a', newline='')
        self.outputCSV = outputCSV
        self.counter = 0
        self.csvWriter = csv.writer(csvfile)

    def write(self, measurements):
        for frameMeasurements in measurements:
            self.writeFrameMeasurement(frameMeasurements)

    def writeFrameMeasurement(self, measurement):
        self.writeRow([measurement.timestamp, measurement.landmark, measurement.x, measurement.y, measurement.z])

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

    def read(self):
        measurement = Measurement(0,'',0,0,0)
        listOfMeasurement = []
        with open(self.outputCSV, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                measurement = Measurement(*line)
                listOfMeasurement.append(measurement)
        # print(listOfMeasurement)
        return listOfMeasurement
