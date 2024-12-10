from blockchain import Blockchain  # Import the Blockchain class from blockchain.py

MAX_MESSAGE_LENGTH = 128  # Set the maximum allowed message length


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
    Main function to handle user input and interaction with the blockchain.
    """
    blockchain = Blockchain()

    print("\n💬 Welcome to YapIt!\n")
    print("The blockchain built by interaction.\n")
    print("For you, by you\n")
    print("Type a message to add it to the blockchain.")
    print(f"(Messages must be between 1 and {MAX_MESSAGE_LENGTH} characters.)")
    print("")
    print("Type 'save' to save the blockchain manually.")
    print("Type 'exit' to disconnect from the blockchain.")
    print("")

    while True:
        try:
            message = input("📝 Your message -> ").strip()
            if message.lower() == 'exit':
                confirm_exit = input("❓ Are you sure you want to disconnect? (yes/no): ").strip().lower()
                if confirm_exit == 'yes':
                    blockchain.save_final_blockchain()
                    print("\n🔗 Final blockchain has been saved to '/data/final_blockchain.txt'.")
                    break
                else:
                    print("✔️ Exit canceled. Continuing...")
                    continue
            elif message.lower() == 'save':
                blockchain.save_final_blockchain()
                print("✔️ Blockchain saved successfully.")
            elif validate_message(message):
                blockchain.add_message(message)
        except KeyboardInterrupt:
            print("\n🔗 Graceful exit detected. Saving blockchain...")
            blockchain.save_final_blockchain()
            print("\n🔗 Final blockchain has been saved to '/data/final_blockchain.txt'.")
            break
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()