import unittest
from src.Rowing_pose_detection.FeedbackProviders.DrivePhase.KneeExtension import KneeExtension
from src.models.Phase import Phase


class KneeExtensionTestCase(unittest.TestCase):
    def testSomething(self):

        # These values should pass the test case: Lean back when extending legs
        # previousHipAngleDuringDrive = 90
        # lastHipAngleDuringDrive = 100
        # previousKneeAngle = 80
        # lastKneeAngleDuringDrive = 120

        # These values should pass the test case: Legs not fully extended
        # previousHipAngleDuringDrive = 70
        # lastHipAngleDuringDrive = 10
        # previousKneeAngleDuringDrive = 240
        # lastKneeAngleDuringDrive = 100

        # Feedback should be empty
        previousHipAngleDuringDrive = 80
        lastHipAngleDuringDrive = 40
        previousKneeAngleDuringDrive = 180
        lastKneeAngleDuringDrive = 160

        feedback = KneeExtension().analyzeData(previousHipAngleDuringDrive, lastHipAngleDuringDrive,
                                               previousKneeAngleDuringDrive, lastKneeAngleDuringDrive)
        self.assertEqual(["Lean back when extending legs"], feedback)
        self.assertEqual(["Legs not fully extended"], feedback)


if __name__ == '__main__':
    unittest.main()
