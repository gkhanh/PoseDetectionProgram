from src.utils.CalculatedAngles import CalculatedAngles


class IsOnRowingMachineCheck:
    def __init__(self) -> None:
        self.bodyAngles = []
        self.result = False

    def onRowingMachineCheck(self, frameMeasurement) -> bool:
        return False
