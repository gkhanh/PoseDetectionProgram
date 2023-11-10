from src.pose_detection.PoseModule import PoseDetector
from src.pose_detection.SquatCounter import SquatRepCounter
from src.utils.CSVWriter import CSVWriter

outputDir = 'D:/MoveLabStudio/Assignment/PoseDetectionPrototype/output/output.csv'


def main():
    poseDetector = PoseDetector()
    # measurements = poseDetector.run()

    csvWriter = CSVWriter(outputDir)
    # csvWriter.write(measurements)

    measurement = csvWriter.read()

    repCounter = SquatRepCounter(measurement)
    result = repCounter.getAllMeasurementInWindowAndCount()
    print(result)


if __name__ == '__main__':
    main()
