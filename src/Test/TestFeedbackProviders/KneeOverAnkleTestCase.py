import unittest
from src.models.Phase import Phase
from src.Rowing_pose_detection.FeedbackProviders.Recovery.KneeOverAnkle import KneeOverAnkle


class KneeOverAnkleTestCase(unittest.TestCase):
    def test_something(self):

        # These values should fail the test
        previousKneeAngleDuringRecovery = 150
        lastKneeAngleDuringRecovery = 90
        lastKneeXCoordinateDuringRecovery = 0.8
        lastAnkleXCoordinateDuringRecovery = 0.64

        # These values should pass the test
        # previousKneeAngleDuringRecovery = 150
        # lastKneeAngleDuringRecovery = 160
        # lastKneeXCoordinateDuringRecovery = 0.3
        # lastAnkleXCoordinateDuringRecovery = 0.64

        feedback = KneeOverAnkle().analyzeData(previousKneeAngleDuringRecovery, lastKneeAngleDuringRecovery, lastKneeXCoordinateDuringRecovery, lastAnkleXCoordinateDuringRecovery)

        self.assertEqual(["Knee must align with ankle"], feedback)


if __name__ == '__main__':
    unittest.main()
