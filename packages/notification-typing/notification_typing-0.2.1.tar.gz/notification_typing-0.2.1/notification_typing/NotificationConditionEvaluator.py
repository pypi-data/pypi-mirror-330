from typing import Dict, Any
from notification_typing.NotificationCondition import NotificationCondition
from notification_typing.NotificationConditionType import NotificationConditionType
from notification_typing.PriceCondition import check_price_condition, valid_price_condition_name
from notification_typing.SignalCondition import check_signal_condition, valid_signal_condition_name
from notification_typing.IndicatorCondition import check_indicator_condition, valid_indicator_condition_name
from logging.config import dictConfig
import logging

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s | %(module)s]: %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S %Z"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            }
        },
        "root": {"level": "DEBUG", "handlers": ["console"]},
    }
)

class ConditionEvaluator:
    def __init__(self, stock_data: Dict[str, Any]):
        self.stock_data = stock_data

    def check_condition(self, condition: NotificationCondition) -> bool:
        """
        Evaluates whether the condition is triggered based on the stock data.
        """
        check_condition_handler = find_condition_handler(condition)
        if check_condition_handler is None:
            return False
        
        condition_type = condition["type"]
        condition_name = condition["condition"]
        target_value = condition["value"]

        logging.debug(f"Evaluating {condition_type} condition: {condition_name} with value: {target_value}")

        return check_condition_handler(condition_name, target_value, self.stock_data)

def find_condition_handler(condition: NotificationCondition):
    condition_type = condition['type']
    condition_name = condition['condition']
    if condition_type == NotificationConditionType.PRICE.value and valid_price_condition_name(condition_name):
        return check_price_condition
    elif condition_type == NotificationConditionType.INDICATOR.value and valid_indicator_condition_name(condition_name):
        return check_indicator_condition
    elif condition_type == NotificationConditionType.SIGNAL.value and valid_signal_condition_name(condition_name):
        return check_signal_condition
    return None

def valid_condition(condition: NotificationCondition) -> bool:
    return find_condition_handler(condition) is not None