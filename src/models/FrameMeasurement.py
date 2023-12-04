# Frame measurement class to store lists of measurement within certain time window
class FrameMeasurement:

    def __init__(self, timestamp, measurements):
        # Store timestamp of the frame
        self.timestamp = timestamp

        # These measurements contain landmarks,x,y,z etc.
        self.measurements = measurements
