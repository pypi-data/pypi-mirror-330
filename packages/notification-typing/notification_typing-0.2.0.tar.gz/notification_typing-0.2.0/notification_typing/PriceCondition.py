from enum import Enum
from typing import Dict, Any
import logging

class PriceCondition(Enum):
    GROW_BY_PCT = "grow_by_pct"
    DEC_BY_PCT = "dec_by_pct"
    GROW_BY_AMT = "grow_by_amt"
    DEC_BY_AMT = "dec_by_amt"
        
def valid_price_condition_name(condition_name):
    return condition_name in [condition.value for condition in PriceCondition]

def check_price_condition(condition_name: str, target_value: float, ticker_info: Dict[str, Any]) -> bool:
    logging.debug(f"Checking price condition {condition_name} with target value {target_value} and ticker info {ticker_info}")
    if condition_name == PriceCondition.GROW_BY_PCT.value:
        return True
    elif condition_name == PriceCondition.DEC_BY_PCT.value:
        return True
    elif condition_name == PriceCondition.GROW_BY_AMT.value:
        return True
    elif condition_name == PriceCondition.DEC_BY_AMT.value:
        return True
    else:
        return False