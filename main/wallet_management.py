# wallet_management.py

import hashlib
import time

def generate_wallet(username):
    """Generates a unique wallet address for a user."""
    unique_string = f"{username}{time.time()}"
    return hashlib.sha256(unique_string.encode()).hexdigest()
