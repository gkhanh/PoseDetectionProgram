import unittest
from src.models.Phase import Phase
from src.Rowing_pose_detection.FeedbackProviders.Recovery.KneeOverAnkle import KneeOverAnkle


class KneeOverAnkleTestCase(unittest.TestCase):
    def test_something(self):

        previousKneeAngle = 150
        currentKneeAngle = 90
        currentKneeXCoordinate = 0.8
        currentAnkleXCoordinate = 0.64

        previousKneeAngle = 150
        currentKneeAngle = 160
        currentKneeXCoordinate = 0.3
        currentAnkleXCoordinate = 0.64

        feedback = KneeOverAnkle().analyzeData(previousKneeAngle, currentKneeAngle, currentKneeXCoordinate, currentAnkleXCoordinate)

        self.assertEqual(["Knee must go over ankle"], feedback)


if __name__ == '__main__':
    unittest.main()
