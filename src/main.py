from src.pose_detection.AngleBasedSquatCounter import AngleBasedSquatCounter
from src.pose_detection.PoseDetector import PoseDetector
from src.pose_detection.PoseDetectorPreviewer import OpenCVPoseDetectorPreviewer, PoseDetectorPreviewer
from src.utils.VideoReader import VideoReader


class MyListener(PoseDetector.Listener):

    def __init__(self, listener):
        self.listener = listener

    def onMeasurement(self, frameMeasurement):
        # self.listener.offerMeasurement(frameMeasurement)
        self.listener.isProperSquat(frameMeasurement)


def main():
    # read the video from source folder
    videoReader = VideoReader("./resources/video3.mp4")

    # real-time video
    # videoReader = VideoReader(0)

    # No video in output
    previewer = PoseDetectorPreviewer()

    # With video in output
    # previewer = OpenCVPoseDetectorPreviewer()

    # angle-based squat counter algorithm
    squatCounter = AngleBasedSquatCounter()
    # write output to csv file
    # csvWriter = CSVWriter("D:/MoveLabStudio/Assignment/PoseDetection-Prototype/output/output2.csv")

    myListener = MyListener(squatCounter)

    poseDetector = PoseDetector(videoReader, previewer, myListener)
    poseDetector.run()


if __name__ == '__main__':
    main()
