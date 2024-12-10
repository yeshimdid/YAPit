from blockchain import Blockchain  # Import the Blockchain class from blockchain.py
from user_management import load_users, register_user, authenticate_user, reset_password  # Import user management functions
from participation_tracker import participation_tracker, PARTICIPATION_STATS_PATH  # Import participation tracking logic
import hashlib
import json

MAX_MESSAGE_LENGTH = 128  # Set the maximum allowed message length

# Encryption key for messages
ENCRYPTION_KEY = "your-secure-key"  # Replace this with a secure key

def encrypt_message(message):
    """
    Encrypts a message using a basic hash-based approach.
    """
    return hashlib.sha256((message + ENCRYPTION_KEY).encode()).hexdigest()

def validate_message(message):
    """
    Validates user input to ensure it's not blank or too long.
    """
    message = message.strip()
    if not message:
        print("⚠️ Message cannot be blank. Please try again.")
        return False
    if len(message) > MAX_MESSAGE_LENGTH:
        print(f"⚠️ Message is too long. Maximum length is {MAX_MESSAGE_LENGTH} characters.")
        return False
    return True

def show_user_status(blockchain, current_user, users):
    """
    Displays the current block number, the user's contribution percentage to the current block,
    and the user's wallet address.
    """
    current_block_index = len(blockchain.chain)  # Current block number

    try:
        # Load participation stats from JSON file
        with open(PARTICIPATION_STATS_PATH, 'r', encoding='utf-8') as f:
            participation_stats = json.load(f)

        # Get user's contributions for the current block
        user_stats = participation_stats.get(current_user, {}).get(str(current_block_index), {})
        user_count = user_stats.get("count", 0)
        user_percentage = user_stats.get("percentage", 0.0)

        # Retrieve the wallet address from user data
        wallet_address = users.get(current_user, {}).get("wallet", "Not available")

        print(f"\n📊 Status for {current_user}:")
        print(f"Wallet Address: {wallet_address}")
        print(f"Current Block Number: {current_block_index}")
        print(f"Your Contributions: {user_count} messages")
        print(f"Your Contribution Percentage: {user_percentage:.2f}%")
    except FileNotFoundError:
        print("⚠️ Participation stats file not found. Unable to retrieve status.")
    except Exception as e:
        print(f"⚠️ Error retrieving status: {e}")

def main():
    """
    Main function to handle user authentication and interaction with the blockchain.
    """
    blockchain = Blockchain()
    users = load_users()

    print("\n💬 Welcome to YapIt!\n")
    print("The blockchain built by interaction.\n")
    print("Type 'register' to create an account.")
    print("Type 'login' to log into an existing account.")
    print("Type 'reset' to reset your password.")
    print("Type 'exit' to quit the program.")

    current_user = None

    while True:
        if not current_user:
            print("\nPlease log in or register to continue.")
            action = input("Choose an action (register/login/reset/exit): ").strip().lower()

            if action == 'register':
                username = input("Enter a username: ").strip()
                password = input("Enter a password: ").strip()
                email = input("Enter your email: ").strip()
                register_user(users, username, password, email)
            elif action == 'login':
                username = input("Enter your username: ").strip()
                password = input("Enter your password: ").strip()
                if authenticate_user(users, username, password):
                    current_user = username
                    print(f"✔️ Welcome, {username}!")
                else:
                    print("❌ Login failed. Please try again.")
            elif action == 'reset':
                email = input("Enter your email: ").strip()
                new_password = input("Enter your new password: ").strip()
                reset_password(users, email, new_password)
            elif action == 'exit':
                print("Exiting...")
                blockchain.save_final_blockchain()
                break
            else:
                print("Invalid action. Please choose 'register', 'login', 'reset', or 'exit'.")

        else:
            print("\nType a message to add it to the blockchain.")
            print(f"(Messages must be between 1 and {MAX_MESSAGE_LENGTH} characters.)")
            print("Type '-status' to check your contribution status.")
            print("Type '-save' to save the blockchain manually.")
            print("Type '-logout' to log out.")
            print("Type '-exit' to disconnect from the blockchain.")

            message = input("📝 Your message -> ").strip()

            if message.lower() == '-status':
                show_user_status(blockchain, current_user, users)
            elif message.lower() == '-logout':
                print(f"✔️ Logged out. Goodbye, {current_user}!")
                current_user = None
            elif message.lower() == '-exit':
                confirm_exit = input("❓ Are you sure you want to disconnect? (yes/no): ").strip().lower()
                if confirm_exit == 'yes':
                    blockchain.save_final_blockchain()
                    print("\n🔗 Final blockchain has been saved.")
                    break
                else:
                    print("✔️ Exit canceled. Continuing...")
                    continue
            elif message.lower() == 'save':
                blockchain.save_final_blockchain()
                print("✔️ Blockchain saved successfully.")
            elif validate_message(message):
                encrypted_message = encrypt_message(message)
                blockchain.add_message(current_user, encrypted_message)

if __name__ == "__main__":
    main()
