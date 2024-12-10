import hashlib
import json
import os
import time

DATA_DIR = '../vip'
USER_DATA_PATH = os.path.join(DATA_DIR, 'users.json')
os.makedirs(DATA_DIR, exist_ok=True)

# Encryption key
ENCRYPTION_KEY = "your-secure-key"  # Replace with a secure key

def encrypt_data(data):
    """Encrypts sensitive data using a hash-based approach."""
    return hashlib.sha256((data + ENCRYPTION_KEY).encode()).hexdigest()

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

def register_user(users, username, password, email):
    """Registers a new user with a hashed password, wallet address, and encrypted email."""
    if username in users:
        print("⚠️ Username already exists.")
        return False
    encrypted_email = encrypt_data(email)
    for details in users.values():
        if details.get("email") == encrypted_email:
            print("⚠️ Email is already associated with another account.")
            return False
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    wallet_address = generate_wallet(username)
    users[username] = {
        "password": hashed_password,
        "wallet": wallet_address,
        "email": encrypted_email
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

def reset_password(users, email, new_password):
    """Resets a user's password if the encrypted email matches."""
    encrypted_email = encrypt_data(email)
    for username, details in users.items():
        if details.get("email") == encrypted_email:
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            users[username]["password"] = hashed_password
            save_users(users)
            print(f"✔️ Password reset successfully for {username}.")
            return True
    print("❌ No user found with that email.")
    return False

if __name__ == "__main__":
    users = load_users()
    print("User Management System")
    while True:
        print("\n1. Register\n2. Login\n3. Reset Password\n4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            username = input("Enter a username: ").strip()
            password = input("Enter a password: ").strip()
            email = input("Enter your email: ").strip()
            register_user(users, username, password, email)
        elif choice == '2':
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            authenticate_user(users, username, password)
        elif choice == '3':
            email = input("Enter your email: ").strip()
            new_password = input("Enter your new password: ").strip()
            reset_password(users, email, new_password)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
