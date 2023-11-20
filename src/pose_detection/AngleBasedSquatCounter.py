from src.utils.CalculatedAngles import CalculatedAngles


# New strategy that uses only angles
class AngleBasedSquatCounter:
    def __init__(self) -> None:
        self.squatAngles = []

    def offerMeasurement(self, frameMeasurement):
        # Filter only RIGHT_KNEE
        angleCalculator = CalculatedAngles([frameMeasurement])
        # calculate hip angle
        result = angleCalculator.calculateHipAngle()
        self.squatAngles.append(result)
