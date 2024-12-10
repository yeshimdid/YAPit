from blockchain import Blockchain  # Import the Blockchain class from blockchain.py
from user_management import load_users, register_user, authenticate_user  # Import user management functions
from participation_tracker import update_participation, calculate_participation_percentage  # Import participation tracker functions
import hashlib

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

def main():
    """
    Main function to handle user authentication and interaction with the blockchain.
    """
    global blockchain
    blockchain = Blockchain()
    users = load_users()

    print("\n💬 Welcome to YapIt!\n")
    print("The blockchain built by interaction.\n")
    print("Type 'register' to create an account.")
    print("Type 'login' to log into an existing account.")
    print("Type 'exit' to quit the program.")

    current_user = None

    while True:
        if not current_user:
            print("\nPlease log in or register to continue.")
            action = input("Choose an action (register/login/exit): ").strip().lower()

            if action == 'register':
                username = input("Enter a username: ").strip()
                password = input("Enter a password: ").strip()
                register_user(users, username, password)
            elif action == 'login':
                username = input("Enter your username: ").strip()
                password = input("Enter your password: ").strip()
                if authenticate_user(users, username, password):
                    current_user = username
                    print(f"✔️ Welcome, {username}!")
                    print(f"💼 Your wallet address: {users[username]['wallet']}")
                else:
                    print("❌ Login failed. Please try again.")
            elif action == 'exit':
                print("Exiting...")
                blockchain.save_final_blockchain()
                break
            else:
                print("Invalid action. Please choose 'register', 'login', or 'exit'.")

        else:
            print("\nType a message to add it to the blockchain.")
            print(f"(Messages must be between 1 and {MAX_MESSAGE_LENGTH} characters.)")
            print("Type 'save' to save the blockchain manually.")
            print("Type 'logout' to log out.")
            print("Type 'exit' to disconnect from the blockchain.")
            print("Type 'participation' to view your participation percentage.")

            message = input("📝 Your message -> ").strip()

            if message.lower() == 'logout':
                print(f"✔️ Logged out. Goodbye, {current_user}!")
                current_user = None
            elif message.lower() == 'exit':
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
            elif message.lower() == 'participation':
                percentage = calculate_participation_percentage(current_user, len(blockchain.chain))
                print(f"💼 Your participation percentage: {percentage:.2f}%")
            elif validate_message(message):
                encrypted_message = encrypt_message(message)
                blockchain.add_message(current_user, encrypted_message)
                # Track user participation
                update_participation(current_user, len(blockchain.chain))

if __name__ == "__main__":
    main()
