from src.utils.CalculatedAngles import CalculatedAngles


class RowingExerciseCounter:
    def __init__(self) -> None:
        self.bodyAngles = []
        self.stage = None
        self.counter = 0

    def offerMeasurement(self, frameMeasurement):
        pass

    def isRecoveryPhase(self):
        return True

    def isDrivePhase(self):
        return True

    def isProperRowingRecoveryStroke(self):
        pass

    def isProperRowingDriveExercise(self):
        pass
