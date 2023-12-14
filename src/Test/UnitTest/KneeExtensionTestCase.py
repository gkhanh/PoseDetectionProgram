import unittest
from src.Rowing_pose_detection.FeedbackProviders.DrivePhase.KneeExtension import KneeExtension
from src.models.Phase import Phase


class KneeExtensionTestCase(unittest.TestCase):
    def testSomething(self):
        previousHipAngle = 90
        currentHipAngle = 100
        previousKneeAngle = 80
        currentKneeAngle = 120

        previousHipAngle = 70
        currentHipAngle = 10
        previousKneeAngle = 240
        currentKneeAngle = 100

        # previousHipAngle = 60
        # currentHipAngle = 90
        # previousKneeAngle = 160
        # currentKneeAngle = 180

        feedback = KneeExtension().analyzeData(previousHipAngle, currentHipAngle, previousKneeAngle, currentKneeAngle)
        self.assertEqual(["Lean back when extending legs"], feedback)  # add assertion here
        # self.assertEqual(["Leg not fully extended"], feedback)


if __name__ == '__main__':
    unittest.main()
