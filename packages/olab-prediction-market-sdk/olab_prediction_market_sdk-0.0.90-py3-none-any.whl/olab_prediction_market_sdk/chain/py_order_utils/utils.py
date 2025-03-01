import math
from eth_utils import to_checksum_address
from string import punctuation
from random import random
from datetime import datetime, timezone
from .model.sides import OrderSide
from decimal import Decimal, ROUND_DOWN

max_int = math.pow(2, 32)


def normalize(s: str) -> str:
    lowered = s.lower()
    for p in punctuation:
        lowered = lowered.replace(p, "")
    return lowered


def normalize_address(address: str) -> str:
    return to_checksum_address(address)


def generate_seed() -> int:
    """
    Pseudo random seed
    """
    now = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    return round(now * random())


def prepend_zx(in_str: str) -> str:
    """
    Prepend 0x to the input string if it is missing
    """
    s = in_str
    if len(s) > 2 and s[:2] != "0x":
        s = f"0x{s}"
    return s


def calculate_order_amounts(price: float, maker_amount: int, side: OrderSide, decimals: int) -> tuple[int, int]:
    """
    Calculate the maker and taker amounts based on the price and side.
    
    Args:
        price: The price of the order (between 0.01 and 0.99)
        maker_amount: The maker amount in base units
        side: The order side (BUY or SELL)
        decimals: The number of decimal places for the currency
        
    Returns:
        tuple[int, int]: A tuple containing (recalculated_maker_amount, taker_amount)
        For BUY: price = taker/maker
        For SELL: price = taker/maker
    """
    if not (0.01 <= price <= 0.99):
        raise ValueError("Price must be between 0.01 and 0.99 (inclusive)")
    
    price_decimal = Decimal(str(price))  # Convert to Decimal for exact arithmetic
    maker_decimal = Decimal(str(maker_amount))
    decimals_decimal = Decimal(str(10 ** (max(2, decimals / 2))))
    
    if side == OrderSide.BUY:
        # For BUY: price = maker/taker
        exact_taker = math.floor(maker_decimal / price_decimal / decimals_decimal) * decimals_decimal
        taker_amount = int(exact_taker)
        
        recalculated_maker_amount = int(taker_amount * price_decimal)
    else:  # SELL
        # For SELL: price = taker/maker
        # Example: if maker_amount = 111000000 and price = 0.29
        # taker_amount should be 111000000 * 0.29 = 32190000
        exact_taker = math.floor(maker_decimal * price_decimal / decimals_decimal) * decimals_decimal
        taker_amount = int(exact_taker)
        
        # Use Decimal for exact division
        recalculated_maker_amount = int(Decimal(str(taker_amount)) / price_decimal)
    
    # Ensure amounts are at least 1
    taker_amount = int(max(1, taker_amount))
    recalculated_maker_amount = int(max(1, recalculated_maker_amount))
    
    print(f"taker_amount: {taker_amount}, recalculated_maker_amount: {recalculated_maker_amount}")
    
    calculated_price = recalculated_maker_amount / taker_amount if side == OrderSide.BUY else taker_amount / recalculated_maker_amount  
    
    if calculated_price > 0.99 or calculated_price < 0.01:
        raise ValueError("invalid taker_amount and recalculated_maker_amount")
    
    return recalculated_maker_amount, taker_amount

