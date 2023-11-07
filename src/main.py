from src.pose_detection.PoseModule import PoseDetector
from src.utils.CSVWriter import CSVWriter
from src.pose_detection.SquatCounter import SquatRepCounter
from src.utils.plotDataFromCSV import CSVProcessor

outputDir = 'D:/MoveLabStudio/Assignment/PoseDetectionPrototype/output/output.csv'

csvWriter = CSVWriter(outputCSV=outputDir)


def myListener(landmark):
    repCounter = SquatRepCounter()
    CSVData = CSVProcessor(csvFile=outputDir)
    repCounter.detectSquatBasedOnLowestPoint(CSVData)
    result = repCounter.countRepetitions(CSVData)
    print(result)


poseDetector = PoseDetector(myListener)
poseDetector.runPoseCheckerWrapper(videoPath='D:/MoveLabStudio/Assignment/PoseDetectionPrototype/resources/video2.mp4')


