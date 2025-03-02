from typing import TypedDict
from NotificationConditionType import NotificationConditionType

class NotificationCondition(TypedDict):
    type: NotificationConditionType
    condition: str  # The specific condition name
    value: float  # e.g., percentage change for GROW_BY_PCT