import hashlib
import json
from typing import Dict
from string import ascii_letters, digits, ascii_lowercase, ascii_uppercase
import random
import re


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


def generate_transaction():
    text = ""
    for _ in range(20):
        text += random.choice(ascii_letters + digits
                              + ascii_lowercase + ascii_uppercase)
    return text


def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None
