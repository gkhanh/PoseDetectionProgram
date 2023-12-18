import unittest
from src.Rowing_pose_detection.FeedbackProviders.Recovery.ArmAndLegMovement import ArmAndLegMovement
from src.models.Phase import Phase


class ArmAndLegMovementTestCase(unittest.TestCase):
    def testSomething(self):

        # these values should pass the test case: Move the handle forward
        # lastElbowAngleDuringDrive = 155
        # lastKneeAngleDuringDrive = 170
        # lastKneeXCoordinateDuringDrive = 0.7
        # previousWristXCoordinateDuringDrive = 0.3
        # lastWristXCoordinateDuringDrive = 0.4

        # Feedback should be blank
        # lastElbowAngleDuringDrive = 80
        # lastKneeAngleDuringDrive = 100
        # lastKneeXCoordinateDuringDrive = 0.8
        # previousWristXCoordinateDuringDrive = 0.3
        # lastWristXCoordinateDuringDrive = 0.2

        # these values should pass the test case: Straighten the arm
        # lastElbowAngleDuringDrive = 85
        # lastKneeAngleDuringDrive = 170
        # lastKneeXCoordinateDuringDrive = 0.42
        # previousWristXCoordinateDuringDrive = 0.36
        # lastWristXCoordinateDuringDrive = 0.31

        # these values should pass the test case: straighten arms until hands over knees
        lastElbowAngleDuringDrive = 155
        lastKneeAngleDuringDrive = 170
        lastKneeXCoordinateDuringDrive = 0.7
        previousWristXCoordinateDuringDrive = 0.5
        lastWristXCoordinateDuringDrive = 0.4

        # Feedback should show nothing
        lastElbowAngleDuringDrive = 432
        lastKneeAngleDuringDrive = 523
        lastKneeXCoordinateDuringDrive = 323
        previousWristXCoordinateDuringDrive = 412
        lastWristXCoordinateDuringDrive = 87

        feedback = ArmAndLegMovement().analyzeData(lastElbowAngleDuringDrive, lastKneeAngleDuringDrive, lastKneeXCoordinateDuringDrive, previousWristXCoordinateDuringDrive,
                                                   lastWristXCoordinateDuringDrive)
        self.assertEqual(["Move the handle forward"], feedback)
        self.assertEqual(["Straighten the arm"], feedback)
        self.assertEqual(["Straighten arms until hands over knees"], feedback)


if __name__ == '__main__':
    unittest.main()
