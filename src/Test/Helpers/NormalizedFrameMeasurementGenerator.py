from src.models.NormalizedFrameMeasurement import NormalizedFrameMeasurement
from src.models.NormalizedMeasurement import NormalizedLandmarkPosition
from src.models.NormalizedMeasurement import NormalizedMeasurement


def createNormalizedFrameMeasurement(
        timestamp,
        shoulder=(0, 0, 0),
        elbow=(0, 0, 0),
        wrist=(0, 0, 0),
        pinky=(0, 0, 0),
        index=(0, 0, 0),
        thumb=(0, 0, 0),
        hip=(0, 0, 0),
        knee=(0, 0, 0),
        ankle=(0, 0, 0),
        heel=(0, 0, 0),
        foot_index=(0, 0, 0),
        eye=(0, 0, 0),
        ear=(0, 0, 0),
        eye_inner=(0, 0, 0),
        eye_outer=(0, 0, 0),
):
    return NormalizedFrameMeasurement(
        timestamp=timestamp,
        normalizedMeasurements=[
            NormalizedMeasurement(timestamp, NormalizedLandmarkPosition.SHOULDER, shoulder[0], shoulder[1],
                                  shoulder[2]),
            NormalizedMeasurement(timestamp, NormalizedLandmarkPosition.ELBOW, elbow[0], elbow[1], elbow[2]),
            NormalizedMeasurement(timestamp, NormalizedLandmarkPosition.WRIST, wrist[0], wrist[1], wrist[2]),
            NormalizedMeasurement(timestamp, NormalizedLandmarkPosition.PINKY, pinky[0], pinky[1], pinky[2]),
            NormalizedMeasurement(timestamp, NormalizedLandmarkPosition.INDEX, index[0], index[1], index[2]),
            NormalizedMeasurement(timestamp, NormalizedLandmarkPosition.THUMB, thumb[0], thumb[1], thumb[2]),
            NormalizedMeasurement(timestamp, NormalizedLandmarkPosition.HIP, hip[0], hip[1], hip[2]),
            NormalizedMeasurement(timestamp, NormalizedLandmarkPosition.KNEE, knee[0], knee[1], knee[2]),
            NormalizedMeasurement(timestamp, NormalizedLandmarkPosition.ANKLE, ankle[0], ankle[1], ankle[2]),
            NormalizedMeasurement(timestamp, NormalizedLandmarkPosition.HEEL, heel[0], heel[1], heel[2]),
            NormalizedMeasurement(timestamp, NormalizedLandmarkPosition.FOOT_INDEX, foot_index[0], foot_index[1],
                                  foot_index[2]),
            NormalizedMeasurement(timestamp, NormalizedLandmarkPosition.EYE, eye[0], eye[1], eye[2]),
            NormalizedMeasurement(timestamp, NormalizedLandmarkPosition.EAR, ear[0], ear[1], ear[2]),
            NormalizedMeasurement(timestamp, NormalizedLandmarkPosition.EYE_INNER, eye_inner[0], eye_inner[1],
                                  eye_inner[2]),
            NormalizedMeasurement(timestamp, NormalizedLandmarkPosition.EYE_OUTER, eye_outer[0], eye_outer[1],
                                  eye_outer[2]),
        ]
    )
