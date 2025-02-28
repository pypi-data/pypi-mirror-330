from enum import Enum

class NotificationType(Enum):
    EMAIL = 1,
    SMS = 2,
    MOBILE = 3
    @classmethod
    def from_string(cls, s):
        try:
            return cls[s]
        except KeyError:
            raise ValueError(f"'{s}' is not a valid NotificationType")

