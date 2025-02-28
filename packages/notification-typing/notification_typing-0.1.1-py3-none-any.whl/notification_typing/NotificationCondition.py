from enum import Enum

class NotificationCondition(Enum):
    GROW_BY_3_PCT = 1, # grew by 3% a day
    DEC_BY_3_PCT = 2, # decrease by 3% a day
    GROW_BY_5_PCT = 1, # grew by 5% a day
    DEC_BY_5_PCT = 2, # decrease by 5% a day
    ## Add more
    @classmethod
    def from_string(cls, s):
        try:
            return cls[s]
        except KeyError:
            raise ValueError(f"'{s}' is not a valid NotificationCondition")

def valid_frequency(condition):
    return condition in NotificationCondition