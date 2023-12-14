import unittest
from src.Rowing_pose_detection.FeedbackProviders.DrivePhase.HipOpening import HipOpening
from src.models.Phase import Phase


class HipOpeningTestCase(unittest.TestCase):
    def testSomething(self):
        currentKneeAngle = 120
        currentHipAngle = 100
        previousHipAngle = 90

        currentKneeAngle = 180
        currentHipAngle = 123
        previousHipAngle = 43

        currentKneeAngle = 473
        currentHipAngle = 123
        previousHipAngle = 90

        # currentKneeAngle = 20
        # currentHipAngle = 64
        # previousHipAngle = 75

        feedback = HipOpening().analyzeData(currentKneeAngle, currentHipAngle, previousHipAngle)
        self.assertEqual(["Open hip too soon"], feedback)
        self.assertEqual(["Hip is not open"], feedback)


if __name__ == '__main__':
    unittest.main()
