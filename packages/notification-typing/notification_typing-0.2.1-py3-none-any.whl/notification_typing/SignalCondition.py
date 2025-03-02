from enum import Enum
from typing import Dict, Any
import logging

class SignalCondition(Enum):
    BUY_SIGNAL = "buy_signal"
    SELL_SIGNAL = "sell_signal"
    
def valid_signal_condition_name(condition_name):
    return condition_name in [condition.value for condition in SignalCondition]

def check_signal_condition(condition_name: str, target_value: float, ticker_info: Dict[str, Any]) -> bool:
    logging.debug(f"Checking signal condition {condition_name} and ticker info {ticker_info}")
    if condition_name == SignalCondition.BUY_SIGNAL.value:
        return True
    elif condition_name == SignalCondition.SELL_SIGNAL.value:
        return True
    else:
        return False