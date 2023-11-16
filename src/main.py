from src.pose_detection.PoseDetector import PoseDetector
from src.pose_detection.PoseDetectorPreviewer import OpenCVPoseDetectorPreviewer
from src.pose_detection.SquatCounter import SquatRepCounter
from src.utils.VideoReader import VideoReader


def main():
    videoReader = VideoReader("./resources/video3.mp4")

    class MyListener(PoseDetector.Listener):

        def __init__(self, squatCounter):
            self.squatCounter = squatCounter

        def onMeasurement(self, measurement):
            self.squatCounter.offerMeasurement(measurement)

    # previewer = PoseDetectorPreviewer()
    previewer = OpenCVPoseDetectorPreviewer()

    squatCounter = SquatRepCounter()

    myListener = MyListener(squatCounter)

    poseDetector = PoseDetector(videoReader, previewer, myListener)
    poseDetector.run()
    # squatCounter.curlCounterLogic()




if __name__ == '__main__':
    main()
