from src.Squat_pose_detection.AngleBasedSquatCounter import AngleBasedSquatCounter
from src.pose_detection.PoseDetector import PoseDetector
from src.pose_detection.PoseDetectorPreviewer import OpenCVPoseDetectorPreviewer
from src.utils.VideoReader import VideoReader
from src.Rowing_pose_detection.IsOnRowingMachineCheck import IsOnRowingMachineCheck
from src.Rowing_pose_detection.DrivePhasePrerequisite import DrivePhasePrerequisite


class PoseListener(PoseDetector.Listener):

    def __init__(self, listener):
        self.listener = listener

    def onMeasurement(self, frameMeasurement):
        # self.listener.isProperSquat(frameMeasurement)
        self.listener.onRowingMachineCheck(frameMeasurement)
        self.listener.Drive(frameMeasurement)


class SquatListener(AngleBasedSquatCounter.Listener):

    def __init__(self, previewer):
        self.previewer = previewer

    def onSquat(self, counter):
        print("Squat count: " + str(counter))
        self.previewer.drawCounter(counter)


class OnRowingMachineListener(IsOnRowingMachineCheck.Listener):

    def __init__(self, previewer):
        self.previewer = previewer

    def onRowingMachineCheck(self, text):
        print("Is on rowing machine: " + str(text))
        self.previewer.displayResult(text)


class DrivePhaseListener(DrivePhasePrerequisite.Listener):

    def __init__(self, previewer):
        self.previewer = previewer

    def drivePhaseCheck(self, text):
        print("Is drive phase: " + str(text))
        self.previewer.displayDrivePhaseChecker(text)


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

    # Squat Detector
    squatCounter = AngleBasedSquatCounter()
    poseDetector.addListener(PoseListener(squatCounter))
    squatCounter.addListener(SquatListener(previewer))

    # Is on rowing machine checker
    onRowingMachineCheck = IsOnRowingMachineCheck()
    poseDetector.addListener(PoseListener(onRowingMachineCheck))
    onRowingMachineCheck.addListener(OnRowingMachineListener(previewer))

    # Drive phase checker
    drivePhasePrerequisite = DrivePhasePrerequisite(OnRowingMachineListener(previewer), poseDetector)

    poseDetector.addListener(PoseListener(drivePhasePrerequisite))
    drivePhasePrerequisite.addListener(DrivePhaseListener(previewer))

    poseDetector.run()


if __name__ == '__main__':
    main()
