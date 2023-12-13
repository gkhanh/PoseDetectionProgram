from src.Rowing_pose_detection.PhaseDetector import PhaseDetector
from src.utils.Cancellable import Cancellable


class RowingFeedbackProvider(PhaseDetector.Listener):

    def __init__(self, phaseDetector, feedbackProviders):
        self.phaseDetector = phaseDetector
        self.feedbackProviders = feedbackProviders

        self.listeners = []
        self.phaseDetectorCancellable = None

    def addListener(self, listener):
        self.listeners.append(listener)

        if len(self.listeners) == 1:
            self.phaseDetectorCancellable = self.phaseDetector.addListener(self)

        return Cancellable(lambda: self.removeListener(listener))

    def removeListener(self, listener):
        self.listeners.remove(listener)

        if len(self.listeners) == 0:
            self.phaseDetectorCancellable.cancel()
            self.phaseDetectorCancellable = None

    def onPhaseChange(self, currentPhase, frameMeasurementBuffer):
        feedback = []

        for feedbackProvider in self.feedbackProviders:
            feedback.append(feedbackProvider.getFeedback(currentPhase, frameMeasurementBuffer))

        for listener in self.listeners:
            listener.onFeedback(feedback)

    class FeedbackProvider:
        def getFeedback(self, currentPhase, frameMeasurementBuffer):
            raise NotImplementedError

    class Listener:
        def onFeedback(self, feedback):
            raise NotImplementedError
