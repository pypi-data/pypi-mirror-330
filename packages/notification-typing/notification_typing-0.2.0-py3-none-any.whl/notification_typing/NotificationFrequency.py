from enum import Enum

class NotificationFrequency(Enum):
    FREQUENT = 'frquent' # 3 times a day
    MODERATE = 'moderate' # 1 time a day
    RARE = 'rare' # 2 times a week

def valid_notification_frequency(notification_frequency):
    return notification_frequency in [frequency.value for frequency in NotificationFrequency]