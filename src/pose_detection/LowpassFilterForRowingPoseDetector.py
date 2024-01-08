from src.pose_detection.PoseDetector import PoseDetector
from src.utils.Cancellable import Cancellable
from src.models.FrameMeasurement import FrameMeasurement
from src.models.Measurement import Measurement
from src.models.Measurement import LandmarkPosition


class LowpassFilterForRowingPoseDetector(PoseDetector.Listener):
    def __init__(self, poseDetector):
        self.poseDetector = poseDetector
        self.listeners = []
        self.coefficient = 0.3
        self.previous = None
        self.poseDetectorCancellable = None

    def onMeasurement(self, frameMeasurement):
        self.previous = self.process(self.previous, frameMeasurement)
        self.notifyListeners(self.previous)

    def process(self, previous, current):
        if previous is None:
            return current
        else:
            current = self.checkIfDatapointExistInPrevious(previous, current)
            return current

    # Function to check if the landmark in current normalizedFrameMeasurement exist in previous normalizedFrameMeasurement
    def checkIfDatapointExistInPrevious(self, previous, current):
        updatedMeasurements = []
        for measurement in current.measurements:
            previousMeasurement = self.findPreviousMeasurement(measurement.landmark, previous)
            if previousMeasurement is not None:

                processedMeasurement = Measurement(
                    measurement.timestamp,
                    measurement.landmark,
                    self.coefficient * measurement.x + (1 - self.coefficient) * previousMeasurement.x,
                    self.coefficient * measurement.y + (1 - self.coefficient) * previousMeasurement.y,
                    self.coefficient * measurement.z + (1 - self.coefficient) * previousMeasurement.z
                )

                updatedMeasurements.append(processedMeasurement)
            else:
                updatedMeasurements.append(measurement)

        return FrameMeasurement(current.timestamp, updatedMeasurements)

    def findPreviousMeasurement(self, landmark, previous):
        for previousMeasurement in previous.measurements:
            if previousMeasurement.landmark == landmark:
                return previousMeasurement
        return None

    def notifyListeners(self, frameMeasurement):
        for listener in self.listeners:
            listener.onMeasurement(frameMeasurement)

    def addListener(self, listener):
        self.listeners.append(listener)
        if len(self.listeners) == 1:
            self.poseDetectorCancellable = self.poseDetector.addListener(self)
        return Cancellable(lambda: self.listeners.remove(listener))

    def removeListener(self, listener):
        self.listeners.remove(listener)
        if len(self.listeners) == 0:
            self.poseDetectorCancellable.cancel()
            self.poseDetectorCancellable = None

    class Listener:
        def onMeasurement(self, frameMeasurement: FrameMeasurement):
            raise NotImplementedError




