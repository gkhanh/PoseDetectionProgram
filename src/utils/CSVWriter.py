import csv

from src.models.measurement import Measurement, LandmarkPosition


class CSVWriter:
    def __init__(self, path):
        csvfile = open(path, 'a', newline='')
        self.path = path
        self.counter = 0
        self.csvWriter = csv.writer(csvfile)

    def write(self, measurements):
        for frameMeasurements in measurements:
            self.writeFrameMeasurement(frameMeasurements)

    def writeFrameMeasurement(self, measurement):
        self.writeRow(
            [measurement.timestamp, self.landmarkPositionToString(measurement.landmark), measurement.x, measurement.y,
             measurement.z])

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
        listOfMeasurement = []
        with open(self.path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                measurement = Measurement(
                    timestamp=float(line[0]),
                    landmark=self.stringToLandmarkPosition(line[1]),
                    x=float(line[2]),
                    y=float(line[3]),
                    z=float(line[4])
                )
                listOfMeasurement.append(measurement)
        return listOfMeasurement

    def landmarkPositionToString(self, landmark):
        switcher = {
            LandmarkPosition.RIGHT_HIP: "RIGHT_HIP",
            LandmarkPosition.RIGHT_KNEE: "RIGHT_KNEE"
        }

        return switcher.get(landmark, "Invalid landmark position")

    def stringToLandmarkPosition(self, landmark):
        switcher = {
            "RIGHT_HIP": LandmarkPosition.RIGHT_HIP,
            "RIGHT_KNEE": LandmarkPosition.RIGHT_KNEE
        }

        return switcher.get(landmark, "Invalid landmark position")
