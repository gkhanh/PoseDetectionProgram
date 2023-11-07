from src.pose_detection.PoseModule import PoseDetector
from src.utils.CSVWriter import CSVWriter

csvWriter = CSVWriter(outputCSV='D:/MoveLabStudio/Assignment/PoseDetectionPrototype/output/output.csv')


def myListener(landmark):
    pass


poseDetector = PoseDetector(
    #myListener
)

poseDetector.runPoseCheckerWrapper(videoPath='D:/MoveLabStudio/Assignment/PoseDetectionPrototype/resources/video2.mp4')
