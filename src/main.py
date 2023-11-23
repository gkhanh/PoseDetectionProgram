from src.pose_detection.AngleBasedSquatCounter import AngleBasedSquatCounter
from src.pose_detection.PoseDetector import PoseDetector
from src.pose_detection.PoseDetectorPreviewer import OpenCVPoseDetectorPreviewer
from src.utils.VideoReader import VideoReader


class PoseListener(PoseDetector.Listener):

    def __init__(self, listener):
        self.listener = listener

    def onMeasurement(self, frameMeasurement):
        self.listener.isProperSquat(frameMeasurement)


class SquatListener(AngleBasedSquatCounter.Listener):

    def __init__(self, previewer):
        self.previewer = previewer

    def onSquat(self, counter):
        print("Squat count: " + str(counter))
        self.previewer.drawCounter(counter)


def main():
    # Video reader, read from video file or pass in 0 to read from camera
    videoReader = VideoReader("./resources/video3.mp4")

    # Previewer, show the video frame or not
    # previewer = PoseDetectorPreviewer()
    previewer = OpenCVPoseDetectorPreviewer()

    # Pose detector, detect the pose from a video feed
    poseDetector = PoseDetector(videoReader, previewer)

    # write output to csv file
    # csvWriter = CSVWriter("D:/MoveLabStudio/Assignment/PoseDetection-Prototype/output/output2.csv")

    # Algorithms
    squatCounter = AngleBasedSquatCounter()
    poseDetector.addListener(PoseListener(squatCounter))

    squatCounter.addListener(SquatListener(previewer))

    poseDetector.run()


if __name__ == '__main__':
    main()
