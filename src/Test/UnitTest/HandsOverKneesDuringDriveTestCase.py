import unittest

from src.Rowing_pose_detection.FeedbackProviders.DrivePhase.HandsOverKneesDuringDrive import HandsOverKneesDuringDrive
from src.Test.Helpers.NormalizedFrameMeasurementGenerator import createNormalizedFrameMeasurement
from src.models.Phase import Phase


class HandsOverKneesDuringDriveTestCase(unittest.TestCase):
    def testSomething(self):
        # Given
        # Feedback should be empty in this case:
        lastShoulderAngleDuringDrive = 25
        lastElbowAngleDuringDrive = 140
        previousWristXCoordinateDuringDrive = 0.56
        lastKneeXCoordinateDuringDrive = 0.32
        lastWristXCoordinateDuringDrive = 0.42

        # These values should pass the test case: Arm not pulled back properly
        # lastShoulderAngleDuringDrive = 12
        # lastElbowAngleDuringDrive = 80
        # previousWristXCoordinateDuringDrive = 0.61
        # lastKneeXCoordinateDuringDrive = 0.6
        # lastWristXCoordinateDuringDrive = 0.57

        # These value should pass the test case: Not pulling arm
        # lastShoulderAngleDuringDrive = 5
        # lastElbowAngleDuringDrive = 50
        # previousWristXCoordinateDuringDrive = 0.4
        # lastKneeXCoordinateDuringDrive = 0.45
        # lastWristXCoordinateDuringDrive = 0.55

        # When
        feedback = HandsOverKneesDuringDrive().analyzeData(lastShoulderAngleDuringDrive, lastElbowAngleDuringDrive,
                                                           previousWristXCoordinateDuringDrive, lastKneeXCoordinateDuringDrive, lastWristXCoordinateDuringDrive)

        # Then
        self.assertEqual(["Arm not pulled back properly"], feedback)
        self.assertEqual(["Not pulling arm"], feedback)


if __name__ == '__main__':
    unittest.main()
