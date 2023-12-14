import unittest
from src.models.Phase import Phase
from src.Rowing_pose_detection.FeedbackProviders.Recovery.BodyPosture import BodyPosture


class BodyPostureTestCase(unittest.TestCase):
    def testSomething(self):

        previousHipAngle = 80
        currentHipAngle = 90
        previousElbowAngle = 120
        currentElbowAngle = 170

        feedback = BodyPosture().analyzeData(previousHipAngle, currentHipAngle, previousElbowAngle, currentElbowAngle)
        self.assertEqual(["Tip your body forward"], feedback)  # add assertion here


if __name__ == '__main__':
    unittest.main()
