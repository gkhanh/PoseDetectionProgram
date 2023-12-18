import unittest
from src.models.Phase import Phase
from src.Rowing_pose_detection.FeedbackProviders.Recovery.BodyPosture import BodyPosture


class BodyPostureTestCase(unittest.TestCase):
    def testSomething(self):

        # previousHipAngleDuringRecovery = 80
        # lastHipAngleDuringRecovery = 90
        # previousElbowAngleDuringRecovery = 120
        # lastElbowAngleDuringRecovery = 170

        # these values should pass the test
        previousHipAngleDuringRecovery = 130
        lastHipAngleDuringRecovery = 120
        previousElbowAngleDuringRecovery = 70
        lastElbowAngleDuringRecovery = 170

        feedback = BodyPosture().analyzeData(previousHipAngleDuringRecovery, lastHipAngleDuringRecovery, previousElbowAngleDuringRecovery, lastElbowAngleDuringRecovery)
        self.assertEqual(["Tip your body forward"], feedback)  # add assertion here


if __name__ == '__main__':
    unittest.main()
