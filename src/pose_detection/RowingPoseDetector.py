from src.pose_detection.PoseDetector import PoseDetector
from src.utils.Cancellable import Cancellable
from src.models.NormalizedFrameMeasurement import NormalizedFrameMeasurement
from src.models.NormalizedMeasurement import NormalizedMeasurement
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.models.FrameMeasurement import FrameMeasurement
from src.models.Measurement import LandmarkPosition
from src.models.Measurement import Measurement


class RowingPoseDetector(PoseDetector.Listener):
    def __init__(self, poseDetector):
        self.poseDetector = poseDetector
        self.poseDetectorCancellable = None
        self.listeners = []

    def onMeasurement(self, frameMeasurement):
        if self.isOnRightSide(frameMeasurement):

            self.notifyListener(self.mapToRight(frameMeasurement))
            # self.notifyListener(self.mapToLeft(reversedMeasurement))
        else:
            reversedMeasurement = self.reverseMeasurement(frameMeasurement)
            self.notifyListener(self.mapToLeft(reversedMeasurement))
            # self.notifyListener(self.mapToRight(frameMeasurement))

    def extractData(self, frameMeasurement):
        leftFootXCoordinate = None
        rightFootXCoordinate = None
        leftHipXCoordinate = None
        rightHipXCoordinate = None
        if frameMeasurement is not None:
            for measurement in frameMeasurement.measurements:
                if measurement.landmark == LandmarkPosition.LEFT_FOOT_INDEX:
                    leftFootXCoordinate = measurement.x
                elif measurement.landmark == LandmarkPosition.RIGHT_FOOT_INDEX:
                    rightFootXCoordinate = measurement.x
                elif measurement.landmark == LandmarkPosition.LEFT_HIP:
                    leftHipXCoordinate = measurement.x
                elif measurement.landmark == LandmarkPosition.RIGHT_HIP:
                    rightHipXCoordinate = measurement.x
        return leftFootXCoordinate, rightFootXCoordinate, leftHipXCoordinate, rightHipXCoordinate

    def reverseMeasurement(self, frameMeasurement):
        reversedMeasurements = []
        if frameMeasurement is not None:
            for measurement in frameMeasurement.measurements:
                # Reverse x-coordinate (assuming the range is from 0 to 1)
                reversedMeasurement = Measurement(
                    measurement.timestamp,
                    measurement.landmark,
                    1 - measurement.x,  # Reverse the x-coordinate
                    measurement.y,
                    measurement.z
                )
                reversedMeasurements.append(reversedMeasurement)
        return FrameMeasurement(frameMeasurement.timestamp, reversedMeasurements)

    def isOnRightSide(self, frameMeasurement):
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

    def isOnLeftSide(self, frameMeasurement):
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

    def mapToRight(self, frameMeasurement):
        normalizedMeasurements = []
        if frameMeasurement is not None:
            for measurement in frameMeasurement.measurements:
                if measurement.landmark.name.startswith('RIGHT_'):
                    # Get the part after 'RIGHT_'
                    landmark = measurement.landmark.name.split('RIGHT_')[-1]

                    try:
                        # Map the string to the Enum value
                        normalizedLandmark = NormalizedLandmarkPosition[landmark]
                        # Create a new NormalizedMeasurement with the normalized landmark
                        normalizedMeasurement = NormalizedMeasurement(
                            timestamp=measurement.timestamp,
                            landmark=normalizedLandmark,
                            x=measurement.x,
                            y=measurement.y,
                            z=measurement.z
                        )
                        normalizedMeasurements.append(normalizedMeasurement)
                    except KeyError:
                        # Handle the case where the landmark is not in the Enum
                        print(f"Invalid landmark: {landmark}")
        return NormalizedFrameMeasurement(frameMeasurement.timestamp, normalizedMeasurements)

    def mapToLeft(self, frameMeasurement):
        normalizedMeasurements = []
        if frameMeasurement is not None:

            for measurement in frameMeasurement.measurements:
                if measurement.landmark.name.startswith('LEFT_'):
                    # Get the part after 'LEFT_'
                    landmark = measurement.landmark.name.split('LEFT_')[-1]

                    try:
                        # Map the string to the Enum value
                        normalizedLandmark = NormalizedLandmarkPosition[landmark]
                        # Create a new NormalizedMeasurement with the normalized landmark
                        normalizedMeasurement = NormalizedMeasurement(
                            timestamp=measurement.timestamp,
                            landmark=normalizedLandmark,
                            x=measurement.x,
                            y=measurement.y,
                            z=measurement.z
                        )
                        normalizedMeasurements.append(normalizedMeasurement)
                    except KeyError:
                        # Handle the case where the landmark is not in the Enum
                        print(f"Invalid landmark: {landmark}")
        return NormalizedFrameMeasurement(frameMeasurement.timestamp, normalizedMeasurements)

    def notifyListeners(self, normalizedFrameMeasurement):
        for listener in self.listeners:
            listener.onMeasurement(normalizedFrameMeasurement)

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

    def notifyListener(self, normalizedFrameMeasurement: NormalizedFrameMeasurement):
        for listener in self.listeners:
            listener.onMeasurement(normalizedFrameMeasurement)

    class Listener:
        def onMeasurement(self, normalizedFrameMeasurement: NormalizedFrameMeasurement):
            raise NotImplementedError
