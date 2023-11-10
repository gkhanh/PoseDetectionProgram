from src.pose_detection.SquatCounter import SquatRepCounter
from src.utils.CSVWriter import CSVWriter


def main():
    # videoReader = VideoReader('../resources/video2.mp4')

    # previewer = PoseDetectorPreviewer()
    # previewer = OpenCVPoseDetectorPreviewer()

    # poseDetector = PoseDetector(videoReader, previewer)
    # measurements = poseDetector.run()

    csvWriter = CSVWriter('../output/output.csv')
    # csvWriter.write(measurements)

    measurements = csvWriter.read()

    repCounter = SquatRepCounter(measurements)
    result = repCounter.getAllMeasurementInWindowAndCount()
    print(result)


if __name__ == '__main__':
    main()
