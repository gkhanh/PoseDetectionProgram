class NormalizedFrameMeasurement:

    def __init__(self, timestamp, normalizedMeasurements):
        # Store timestamp of the frame
        self.timestamp = timestamp

        # These measurements contain landmarks,x,y,z etc.
        self.normalizedMeasurements = normalizedMeasurements
