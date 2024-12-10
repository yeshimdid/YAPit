import hashlib
import os
import time

# Update the directory path to use the 'vip' directory, relative to the 'main' folder
DATA_DIR = '../vip'
os.makedirs(DATA_DIR, exist_ok=True)

class Block:
    """Represents a single block in the blockchain."""
    def __init__(self, index, messages, previous_hash, timestamp=None):
        self.index = index
        self.messages = messages
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculates the hash of the block's contents."""
        block_content = f"{self.index}{''.join(self.messages)}{self.previous_hash}{self.timestamp}"
        return hashlib.sha256(block_content.encode()).hexdigest()

class Blockchain:
    """Manages the entire blockchain and message handling logic."""
    PENDING_MESSAGES_PATH = os.path.join(DATA_DIR, 'pending_messages.txt')
    FINAL_BLOCKCHAIN_PATH = os.path.join(DATA_DIR, 'final_blockchain.txt')

    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_messages = self.load_pending_messages()

    def create_genesis_block(self):
        """Creates the first block (Genesis block) in the blockchain."""
        return Block(0, ["Genesis Block"], "0")
    
    def test_file_write(self):
        """Directly writes a test line to 'pending_messages.txt' to check file writing capability."""
        try:
            with open(self.PENDING_MESSAGES_PATH, 'w') as f:
                f.write("Test message for direct write\n")
            print(f"Direct write test successful: File written at {self.PENDING_MESSAGES_PATH}")
        except Exception as e:
            print(f"Direct write test failed: {e}")

    def add_message(self, message):
        """Adds a new message to the pending messages and checks if a new block can be mined."""
        self.pending_messages.append(message)
        print(f"Added message: {message}")
        print(f"Total pending messages: {len(self.pending_messages)}")
        self.check_mine_block()
        self.save_pending_messages()  # Force save after adding a message

    def check_mine_block(self):
        """Checks if the pending messages meet the mining requirement and mines a block if true."""
        messages_needed = self.get_message_requirement()
        if len(self.pending_messages) >= messages_needed:
            self.mine_block()

    def get_message_requirement(self):
        """Calculates the number of messages required to mine the next block."""
        block_index = len(self.chain)
        return 100 * (2 ** ((block_index - 1) // 3))

    def mine_block(self):
        """Mines a new block using the pending messages."""
        previous_block = self.chain[-1]
        messages_needed = self.get_message_requirement()
        new_block = Block(len(self.chain), self.pending_messages[:messages_needed], previous_block.hash)
        self.chain.append(new_block)
        print(f"Mined new block: {new_block.hash}")
        self.pending_messages = self.pending_messages[messages_needed:]
        self.save_final_blockchain()

    def save_pending_messages(self):
        """Saves all pending messages to a file."""
        if self.pending_messages:
            with open(self.PENDING_MESSAGES_PATH, 'w', encoding='utf-8') as f:
                for message in self.pending_messages:
                    f.write(message + "\n")
            print(f"Saved {len(self.pending_messages)} pending messages to '{self.PENDING_MESSAGES_PATH}'.")
        else:
            print("No pending messages to save.")

    def load_pending_messages(self):
        """Loads pending messages from a file, if available."""
        try:
            with open(self.PENDING_MESSAGES_PATH, 'r', encoding='utf-8') as f:
                messages = [line.strip() for line in f.readlines()]
            return messages
        except FileNotFoundError:
            print("No pending messages file found, starting fresh.")
            return []
        except Exception as e:
            print(f"Failed to load pending messages: {e}")

    def save_final_blockchain(self):
        """Saves the full blockchain to a file."""
        try:
            with open(self.FINAL_BLOCKCHAIN_PATH, 'w', encoding='utf-8') as f:
                for block in self.chain:
                    f.write(f"Block {block.index}:\n")
                    f.write(f"Timestamp: {time.ctime(block.timestamp)}\n")
                    f.write(f"Messages ({len(block.messages)} total):\n")
                    for msg in block.messages:
                        f.write(f"  - {msg}\n")
                    f.write(f"Previous Hash: {block.previous_hash}\n")
                    f.write(f"Hash: {block.hash}\n")
                    f.write("\n")  # Add a newline for spacing between blocks
            print(f"Saved final blockchain to {self.FINAL_BLOCKCHAIN_PATH}")
        except Exception as e:
            print(f"Failed to save final blockchain: {e}")

