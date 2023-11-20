from src.pose_detection.AngleBasedSquatCounter import AngleBasedSquatCounter
from src.pose_detection.PoseDetector import PoseDetector
from src.pose_detection.PoseDetectorPreviewer import OpenCVPoseDetectorPreviewer
from src.pose_detection.PoseDetectorPreviewer import PoseDetectorPreviewer
from src.pose_detection.SquatCounter import SquatRepCounter
from src.utils.VideoReader import VideoReader
from src.utils.CSVWriter import CSVWriter


class MyListener(PoseDetector.Listener):

    def __init__(self, listener):
        self.listener = listener

    def onMeasurement(self, frameMeasurement):
        self.listener.offerMeasurement(frameMeasurement)


def main():
    videoReader = VideoReader("D:/MoveLabStudio/Assignment/PoseDetection-Prototype/resources/video2.mp4")

    # No video in output
    previewer = PoseDetectorPreviewer()

    # With video in output
    # previewer = OpenCVPoseDetectorPreviewer()

    # squatCounter = SquatRepCounter()
    squatCounter = AngleBasedSquatCounter()
    # csvWriter = CSVWriter("D:/MoveLabStudio/Assignment/PoseDetection-Prototype/output/output2.csv")

    myListener = MyListener(squatCounter)

    poseDetector = PoseDetector(videoReader, previewer, myListener)
    poseDetector.run()


if __name__ == '__main__':
    main()
