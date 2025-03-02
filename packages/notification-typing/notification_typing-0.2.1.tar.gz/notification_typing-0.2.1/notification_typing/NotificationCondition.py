from typing import TypedDict
from notification_typing.NotificationConditionType import NotificationConditionType

class NotificationCondition(TypedDict):
    type: NotificationConditionType
    condition: str  # The specific condition name
    value: float  # e.g., percentage change for GROW_BY_PCT