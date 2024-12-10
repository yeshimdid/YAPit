import hashlib
import json
import os
import time  # For generating wallet addresses

DATA_DIR = '../vip'
USER_DATA_PATH = os.path.join(DATA_DIR, 'users.json')
os.makedirs(DATA_DIR, exist_ok=True)

def save_users(users):
    """Saves the user database to a file."""
    with open(USER_DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4)
    print("✔️ User database saved.")

def load_users():
    """Loads the user database from a file, if available."""
    try:
        with open(USER_DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("No user database found, starting fresh.")
        return {}
    except Exception as e:
        print(f"Failed to load users: {e}")
        return {}

def generate_wallet(username):
    """Generates a unique wallet address for a user."""
    unique_string = f"{username}{time.time()}"
    return hashlib.sha256(unique_string.encode()).hexdigest()

def register_user(users, username, password):
    """Registers a new user with a hashed password and wallet address."""
    if username in users:
        print("⚠️ Username already exists.")
        return False
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    wallet_address = generate_wallet(username)
    users[username] = {
        "password": hashed_password,
        "wallet": wallet_address
    }
    save_users(users)
    print(f"✔️ User '{username}' registered successfully.")
    print(f"💼 Wallet Address: {wallet_address}")
    return True

def authenticate_user(users, username, password):
    """Authenticates a user by verifying the password."""
    if username not in users:
        print("⚠️ User does not exist.")
        return False
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if users[username]["password"] == hashed_password:
        print("✔️ Authentication successful.")
        print(f"💼 Wallet Address: {users[username]['wallet']}")
        return True
    else:
        print("❌ Invalid password.")
        return False

# Example usage
if __name__ == "__main__":
    users = load_users()
    print("User Management System")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            username = input("Enter a username: ").strip()
            password = input("Enter a password: ").strip()
            register_user(users, username, password)
        elif choice == '2':
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            authenticate_user(users, username, password)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")