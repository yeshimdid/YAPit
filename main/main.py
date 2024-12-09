from blockchain import Blockchain  # Import the Blockchain class from blockchain.py

def main():
    """Main function to handle user input and interaction with the blockchain."""
    blockchain = Blockchain()

    print("\n💬 Welcome to YapIt!\n")
    print("The blockchain built by interaction.\n")
    print("For you, by you\n")
    print("Type a message to add it to the blockchain.")
    print("Type 'exit' to disconnect from the blockchain.")

    while True:
        try:
            message = input("📝 Your message: ")
            if message.lower() == 'exit':
                blockchain.save_final_blockchain()
                print("\n🔗 Final blockchain has been saved to '/data/final_blockchain.txt'.")
                break
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
