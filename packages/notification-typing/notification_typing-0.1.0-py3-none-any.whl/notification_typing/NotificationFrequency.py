from enum import Enum

class NotificationFrequency(Enum):
    FREQUENT = 1, # 3 times a day
    MODERATE = 2, # 1 time a day
    RARE = 3 # 2 times a week
    @classmethod
    def from_string(cls, s):
        try:
            return cls[s]
        except KeyError:
            raise ValueError(f"'{s}' is not a valid NotificationFrequency")

def valid_frequency(frequency):
    return frequency in NotificationFrequency