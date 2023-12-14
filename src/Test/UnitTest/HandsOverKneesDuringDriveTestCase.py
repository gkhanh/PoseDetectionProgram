import unittest

from src.Rowing_pose_detection.FeedbackProviders.DrivePhase.HandsOverKneesDuringDrive import HandsOverKneesDuringDrive
from src.Test.Helpers.NormalizedFrameMeasurementGenerator import createNormalizedFrameMeasurement
from src.models.Phase import Phase


class HandsOverKneesDuringDriveTestCase(unittest.TestCase):
    def testSomething(self):
        # Given
        currentShoulderAngle = 5
        currentElbowAngle = 50
        previousWristXCoordinate = 0.4
        currentKneeXCoordinate = 0.7
        currentWristXCoordinate = 0.55

        # When
        feedback = HandsOverKneesDuringDrive().analyzeData(currentShoulderAngle, currentElbowAngle, previousWristXCoordinate, currentKneeXCoordinate, currentWristXCoordinate)

        # Then
        self.assertEqual(["Arm not pulled back properly"], feedback)
        self.assertEqual(["Not pulling arm"], feedback)


if __name__ == '__main__':
    unittest.main()
