from src.utils.CSVWriter import CSVWriter
from src.pose_detection.PoseModule import PoseDetector
from src.pose_detection.SquatCounter import SquatRepCounter

repCounter = SquatRepCounter()
csvWriter = CSVWriter(outputCSV='C:\Woodchop\Pose_Detection_Program\output\output.csv')
csvWriter.writeColumns()


def myListener(landmark):
    repCounter.offerMeasurement(landmark)


poseDetector = PoseDetector(
    myListener
)

poseDetector.runPoseCheckerWrapper(videoPath='./resources/video2.mp4')
