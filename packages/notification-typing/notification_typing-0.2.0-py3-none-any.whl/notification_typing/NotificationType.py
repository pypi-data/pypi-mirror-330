from enum import Enum

class NotificationType(Enum):
    EMAIL = 'email'
    SMS = 'sms'
    MOBILE = 'mobile'

def valid_notification_type(notification_type):
    return notification_type in [notification_type.value for notification_type in NotificationType]