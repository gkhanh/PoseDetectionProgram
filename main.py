from CSVWriter import CSVWriter
from PoseModule import PoseDetector
from SquatCounter import RepCounter

repCounter = RepCounter()
csvWriter = CSVWriter(outputCSV='./output/output.csv')


def myListener(landmark):
    result = csvWriter.addLine(landmark)
    repCounter.offerMeasurement(landmark)


poseDetector = PoseDetector(
    0,
    myListener
)
poseDetector.extractingLandmark()
