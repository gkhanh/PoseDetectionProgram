import csv


class CSVWriter:
    def __init__(self, outputCSV):
        csvfile = open(outputCSV, 'w', newline='')
        self.counter = 0
        self.csvWriter = csv.writer(csvfile)
        self.csvWriter.writerow(['frameNumber', 'landmark', 'x', 'y', 'z'])

    def addLine(self, line):
        if self.counter < 1000:
            self.csvWriter.writerow(line)
            self.counter += 1
            return line


