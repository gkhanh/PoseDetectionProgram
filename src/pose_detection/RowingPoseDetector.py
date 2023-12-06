from src.pose_detection.PoseDetector import PoseDetector
from src.pose_detection.PoseDetector import FrameMeasurement
from src.pose_detection.PoseDetector import Cancellable


class RowingPoseDetector(PoseDetector.Listener):
    def __init__(self):

        self.listeners = []

    def onMeasurement(self, frameMeasurement):
        if self.isOnLeftSide():
            self.notifyListener(self.reverseMeasurement(frameMeasurement))
        elif self.isOnRightSide():
            self.notifyListener(frameMeasurement)

    def extractData(self, frameMeasurement):
        leftFootXCoordinate = None
        rightFootXCoordinate = None
        leftHipXCoordinate = None
        rightHipXCoordinate = None
        for measurement in frameMeasurement:
            if measurement.landmark == LandmarkPosition.LEFT_FOOT:
                leftFootXCoordinate = measurement.x
            elif measurement.landmark == LandmarkPosition.RIGHT_FOOT:
                rightFootXCoordinate = measurement.x
            elif measurement.landmark == LandmarkPosition.LEFT_HIP:
                leftHipXCoordinate = measurement.x
            elif measurement.landmark == LandmarkPosition.RIGHT_HIP:
                rightHipXCoordinate = measurement.x
        return leftFootXCoordinate, rightFootXCoordinate, leftHipXCoordinate, rightHipXCoordinate

    def isOnRightSide(self):
        data = self.extractData(frameMeasurement)
        leftFootXCoordinate = data[0]
        rightFootXCoordinate = data[1]
        leftHipXCoordinate = data[2]
        rightHipXCoordinate = data[3]

        if leftFootXCoordinate is not None and rightFootXCoordinate is not None and leftHipXCoordinate is not None and rightHipXCoordinate is not None:
            if leftFootXCoordinate > leftHipXCoordinate or rightFootXCoordinate > rightHipXCoordinate:
                return True
            else:
                return False

    def isOnLeftSide(self):
        data = self.extractData(frameMeasurement)
        leftFootXCoordinate = data[0]
        rightFootXCoordinate = data[1]
        leftHipXCoordinate = data[2]
        rightHipXCoordinate = data[3]

        if leftFootXCoordinate is not None and rightFootXCoordinate is not None and leftHipXCoordinate is not None and rightHipXCoordinate is not None:
            if leftFootXCoordinate < leftHipXCoordinate or rightFootXCoordinate < rightHipXCoordinate:
                return True
            else:
                return False

    def reverseMeasurement(self, frameMeasurement):
        if self.isOnLeftSide():
            reversedMeasurements = []
            for measurement in frameMeasurement.measurements:
                # Reverse x-coordinate (assuming the range is from -1 to 1)
                reversedMeasurement = Measurement(
                    measurement.timestamp,
                    measurement.landmark,
                    -measurement.x,  # Reverse the x-coordinate
                    measurement.y,
                    measurement.z
                )
                reversedMeasurements.append(reversedMeasurement)
            return FrameMeasurement(frameMeasurement.timestamp, reversedMeasurements)
        else:
            # No need to reverse
            return frameMeasurement

    def addListener(self, listener):
        self.listeners.append(listener)
        return Cancellable(lambda: self.listeners.remove(listener))

    def notifyListener(self, frameMeasurement):
        for listener in self.listeners:
            listener.onMeasurement(frameMeasurement)

    class Listener:
        def onMeasurement(self, frameMeasurement: FrameMeasurement):
            raise NotImplementedError
