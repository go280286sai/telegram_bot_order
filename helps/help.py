import hashlib
import json
from typing import Dict


def hash_password(password):
    """
    Hash a password.
    :param password:
    :return:
    """
    return hashlib.sha256(password.encode()).hexdigest()


def parse_cart(cart: str) -> Dict[int, int]:
    """
    Parse a cart.
    :param cart:
    :return:
    """
    try:
        cart_items = json.loads(cart)
        if not isinstance(cart_items, dict):
            cart_items = {}
    except json.JSONDecodeError:
        cart_items = {}
    return {int(k): v for k, v in cart_items.items()}
