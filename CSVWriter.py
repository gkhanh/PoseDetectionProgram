import csv


class CSVWriter:
    def __init__(self, outputCSV):
        csvfile = open(outputCSV, 'w', newline='')
        self.csvWriter = csv.writer(csvfile)
        self.csvWriter.writerow(['frameNumber', 'landmark', 'x', 'y', 'z'])

    def addLine(self, line):
        self.csvWriter.writerow(line)
