import csv

class CSVWriter:
    def __init__(self, outputCSV):
        csvfile = open(outputCSV, 'w', newline='')
        self.counter = 0
        self.csvWriter = csv.writer(csvfile)

    def writeRow(self, row: list):
        self.csvWriter.writerow(row)

    # Instead of writing to csv with a list, use Objects or List of objects for rows
    def writeColumns(self):
        self.csvWriter.writerow(['frameNumber', 'landmark', 'x', 'y', 'z'])


    def addLine(self, line):
        if self.counter < 1000:
            self.csvWriter.writerow(line)
            self.counter += 1
            return line


