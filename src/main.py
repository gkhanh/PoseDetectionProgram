# Pose Detection prerequisite
from src.utils.VideoReader import VideoReader
from src.pose_detection.PoseDetector import PoseDetector
from src.pose_detection.PoseDetectorPreviewer import OpenCVPoseDetectorPreviewer

# For rowing pose detection
from src.Rowing_pose_detection.IsOnRowingMachineCheck import IsOnRowingMachineCheck
from src.pose_detection.RowingPoseDetector import RowingPoseDetector
from src.Rowing_pose_detection.PhaseDetector import PhaseDetector
from src.Rowing_pose_detection.RowingFeedbackProvider import RowingFeedbackProvider
from src.pose_detection.LowpassFilterForRowingPoseDetector import LowpassFilterForRowingPoseDetector

# For feedback message for incorrect rowing posture
from src.Rowing_pose_detection.FeedbackProviders.DrivePhase.HandsOverKneesDuringDrive import HandsOverKneesDuringDrive
from src.Rowing_pose_detection.FeedbackProviders.DrivePhase.HipOpening import HipOpening
from src.Rowing_pose_detection.FeedbackProviders.DrivePhase.KneeExtension import KneeExtension

# For feedback message for recovery phase
from src.Rowing_pose_detection.FeedbackProviders.Recovery.ArmAndLegMovement import ArmAndLegMovement
from src.Rowing_pose_detection.FeedbackProviders.Recovery.BodyPosture import BodyPosture
from src.Rowing_pose_detection.FeedbackProviders.Recovery.KneeOverAnkle import KneeOverAnkle

# For squat pose detection
from src.Squat_pose_detection.AngleBasedSquatCounter import AngleBasedSquatCounter

# For output
from src.utils.CSVWriter import CSVWriter


class PoseListener(PoseDetector.Listener):

    def __init__(self, listener):
        self.listener = listener

    def onMeasurement(self, frameMeasurement):
        # self.listener.isProperSquat(frameMeasurement)
        self.listener.onMeasurement(frameMeasurement)


class ProcessedPoseDetectorListener(LowpassFilterForRowingPoseDetector.Listener):

    def __init__(self, previewer):
        self.previewer = previewer

    def onMeasurement(self, frameMeasurement):
        self.previewer.drawFrameMeasurement(frameMeasurement)


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


class RowingStrokeAnalyzer(RowingFeedbackProvider.Listener):
    def __init__(self, previewer):
        self.previewer = previewer

    def onFeedback(self, feedback):
        feedbackString = ""
        for feedbackItem in feedback:
            feedbackString += str(feedbackItem) + "\n"
        self.previewer.displayResult(feedbackString)


def main():
    # Video reader, read from video file or pass in 0 to read from camera
    videoReader = VideoReader("./resources/video.mp4")
    # videoReader = VideoReader(0)

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

    # processedPoseDetector = LowpassFilterForRowingPoseDetector(poseDetector)
    #
    # processedPoseDetector.addListener(ProcessedPoseDetectorListener(previewer))
    #
    # # Is on rowing machine checker
    # rowingPoseDetector = RowingPoseDetector(processedPoseDetector)
    # onRowingMachineCheck = IsOnRowingMachineCheck(rowingPoseDetector)
    #
    # # Drive phase checker
    # phaseDetector = PhaseDetector(onRowingMachineCheck, rowingPoseDetector)
    # phaseDetector.addListener(PhaseListener(previewer))
    #
    # rowingFeedbackProvider = RowingFeedbackProvider(phaseDetector, [
    #     # Drive rules:
    #     HandsOverKneesDuringDrive(),
    #     HipOpening(),
    #     KneeExtension(),
    #     # Recovery rules:
    #     ArmAndLegMovement(),
    #     BodyPosture(),
    #     KneeOverAnkle()
    # ])
    # rowingFeedbackProvider.addListener(RowingStrokeAnalyzer(previewer))

    poseDetector.run()


if __name__ == '__main__':
    main()
