from src.Rowing_pose_detection.PhaseDetector import PhaseDetector
from src.Rowing_pose_detection.DriveTechniqueAnalyzer import DriveTechniqueAnalyzer
from src.Rowing_pose_detection.RecoveryTechniqueAnalyzer import RecoveryTechniqueAnalyzer
from src.Squat_pose_detection.AngleBasedSquatCounter import AngleBasedSquatCounter
from src.pose_detection.PoseDetector import PoseDetector
from src.pose_detection.PoseDetectorPreviewer import OpenCVPoseDetectorPreviewer
from src.utils.VideoReader import VideoReader
from src.Rowing_pose_detection.IsOnRowingMachineCheck import IsOnRowingMachineCheck
from src.pose_detection.RowingPoseDetector import RowingPoseDetector
from src.models.NormalizedMeasurement import NormalizedMeasurement
from src.models.NormalizedFrameMeasurement import NormalizedFrameMeasurement


class PoseListener(PoseDetector.Listener):

    def __init__(self, listener):
        self.listener = listener

    def onMeasurement(self, frameMeasurement):
        # self.listener.isProperSquat(frameMeasurement)
        self.listener.onMeasurement(frameMeasurement)


class SquatListener(AngleBasedSquatCounter.Listener):

    def __init__(self, previewer):
        self.previewer = previewer

    def onSquat(self, counter):
        print("Squat count: " + str(counter))
        self.previewer.drawCounter(counter)


class PhaseListener(PhaseDetector.Listener):

    def __init__(self, previewer):
        self.previewer = previewer

    def onPhaseChange(self, phase, frameMeasurementBuffer):
        self.previewer.displayDrivePhaseChecker(phase)


class RowingStrokeAnalyzer(DriveTechniqueAnalyzer.Listener, RecoveryTechniqueAnalyzer.Listener):
    def __init__(self, previewer):
        self.previewer = previewer

    def driveTechniqueAnalyzer(self, feedbackMessage):
        self.previewer.displayResult(feedbackMessage)

    def recoveryTechniqueAnalyzer(self, feedbackMessage):
        self.previewer.displayResult(feedbackMessage)
        pass


def main():
    # Video reader, read from video file or pass in 0 to read from camera
    videoReader = VideoReader("./resources/rp3_720p.mp4")
    # videoReader = VideoReader(0)

    # Previewer, show the video frame or not
    # previewer = PoseDetectorPreviewer()
    previewer = OpenCVPoseDetectorPreviewer()

    # Pose detector, detect the pose from a video feed
    poseDetector = PoseDetector(videoReader, previewer)

    # write output to csv file
    # csvWriter = CSVWriter("D:/MoveLabStudio/Assignment/PoseDetection-Prototype/output/output2.csv")

    # Squat Detector
    # squatCounter = AngleBasedSquatCounter()
    # poseDetector.addListener(PoseListener(squatCounter))
    # squatCounter.addListener(SquatListener(previewer))

    # Is on rowing machine checker
    rowingPoseDetector = RowingPoseDetector(poseDetector)
    onRowingMachineCheck = IsOnRowingMachineCheck(rowingPoseDetector)

    # Drive phase checker
    drivePhaseDetector = PhaseDetector(onRowingMachineCheck, rowingPoseDetector)
    drivePhaseDetector.addListener(PhaseListener(previewer))
    # drivePhaseAnalyzer = DriveTechniqueAnalyzer(drivePhaseDetector, rowingPoseDetector)
    # drivePhaseAnalyzer.addListener(RowingStrokeAnalyzer(previewer))

    poseDetector.run()


if __name__ == '__main__':
    main()
