from enum import Enum


class Phase(Enum):
    CATCH = 1
    DRIVE_PHASE = 2
    RELEASE = 3
    RECOVERY_PHASE = 4

    # TODO get rid of this as soon as we know how to detect catch and release
    OTHER = 5
