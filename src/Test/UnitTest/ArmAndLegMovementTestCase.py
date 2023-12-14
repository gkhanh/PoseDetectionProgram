import unittest
from src.Rowing_pose_detection.FeedbackProviders.Recovery.ArmAndLegMovement import ArmAndLegMovement
from src.models.Phase import Phase


class ArmAndLegMovementTestCase(unittest.TestCase):
    def testSomething(self):
        currentElbowAngle = 155
        currentKneeAngle = 170
        currentKneeXCoordinate = 0.7
        previousWristXCoordinate = 0.5
        currentWristXCoordinate = 0.6

        # currentElbowAngle = 155
        # currentKneeAngle = 170
        # currentKneeXCoordinate = 0.7
        # previousWristXCoordinate = 0.5
        # currentWristXCoordinate = 0.6

        currentElbowAngle = 155
        currentKneeAngle = 170
        currentKneeXCoordinate = 0.7
        previousWristXCoordinate = 0.5
        currentWristXCoordinate = 0.6

        feedback = ArmAndLegMovement().analyzeData(currentElbowAngle, currentKneeAngle, currentKneeXCoordinate, previousWristXCoordinate,
                                                   currentWristXCoordinate)
        self.assertEqual(["Move the handle forward"], feedback)
        self.assertEqual(["Straighten the arm"], feedback)
        self.assertEqual(["Tip your body forward"], feedback)
        self.assertEqual(["Straighten arms until hands over knees"], feedback)


if __name__ == '__main__':
    unittest.main()
