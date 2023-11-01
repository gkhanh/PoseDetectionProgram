from PoseModule import PoseDetector
from SquatCounter import RepCounter

repCounter = RepCounter()

poseDetector = PoseDetector(
    'media/video2.mp4',
    lambda landmark: repCounter.offerMeasurement(landmark)
)
poseDetector.processVideo()


