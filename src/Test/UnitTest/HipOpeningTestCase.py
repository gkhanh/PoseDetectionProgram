import unittest
from src.Rowing_pose_detection.FeedbackProviders.DrivePhase.HipOpening import HipOpening
from src.models.Phase import Phase


class HipOpeningTestCase(unittest.TestCase):
    def testSomething(self):

        # These values should pass the test: Open hip too soon
        # lastKneeAngleDuringDrive = 120
        # lastHipAngleDuringDrive = 100
        # previousHipAngleDuringDrive = 90

        # These values should pass the test: Hip is not open
        # lastKneeAngleDuringDrive = 180
        # lastHipAngleDuringDrive = 60
        # previousHipAngleDuringDrive = 73

        # Feedback should be empty
        # lastKneeAngleDuringDrive = 160
        # lastHipAngleDuringDrive = 110
        # previousHipAngleDuringDrive = 120

        # Feedback should be empty
        # lastKneeAngleDuringDrive = 473
        # lastHipAngleDuringDrive = 123
        # previousHipAngleDuringDrive = 90

        # These values should pass the test: Hip is not open
        lastKneeAngleDuringDrive = 20
        lastHipAngleDuringDrive = 64
        previousHipAngleDuringDrive = 75

        feedback = HipOpening().analyzeData(lastKneeAngleDuringDrive, lastHipAngleDuringDrive, previousHipAngleDuringDrive)
        self.assertEqual(["Open hip too soon"], feedback)
        self.assertEqual(["Hip is not open"], feedback)


if __name__ == '__main__':
    unittest.main()
