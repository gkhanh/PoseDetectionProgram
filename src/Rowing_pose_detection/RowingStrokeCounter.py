class RowingExerciseCounter:
    def __init__(self) -> None:
        self.bodyAngles = []
        self.stage = None
        self.counter = 0

    def offerMeasurement(self, frameMeasurement):
        pass

    def isRecoveryPhase(self):
        return False

    def isDrivePhase(self):
        return False

    def isProperRowingRecoveryStroke(self):
        pass

    def isProperRowingDriveExercise(self):
        pass
