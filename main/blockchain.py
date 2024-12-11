import hashlib
import os
import time
import json
from participation_tracker import update_participation, save_participation_stats, load_participation_stats

# Set up the directory for storing non-Python files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
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
        # Load participation stats on startup
        load_participation_stats()
        self.chain = [self.create_genesis_block()]
        self.pending_messages = self.load_pending_messages()
        print(f"Blockchain initialized with {len(self.chain)} blocks.")

    def create_genesis_block(self):
        """Creates the first block (Genesis block) in the blockchain."""
        return Block(0, ["Genesis Block"], "0")

    def add_message(self, username, message):
        """Adds a new message to the pending messages with the user's username."""
        self.pending_messages.append({"username": username, "message": message})
        update_participation(username, len(self.chain))  # Track participation for the current block
        self.check_mine_block()
        self.save_pending_messages()

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
        messages = [msg["message"] for msg in self.pending_messages[:messages_needed]]
        new_block = Block(len(self.chain), messages, previous_block.hash)
        self.chain.append(new_block)
        print(f"Mined new block: {new_block.hash}")
        self.pending_messages = self.pending_messages[messages_needed:]
        save_participation_stats()  # Save participation stats for the mined block
        self.save_final_blockchain()
        self.save_pending_messages()

    def save_pending_messages(self):
        """Saves all pending messages to a file."""
        try:
            if self.pending_messages:
                with open(self.PENDING_MESSAGES_PATH, 'w', encoding='utf-8') as f:
                    for message in self.pending_messages:
                        f.write(json.dumps(message) + "\n")
                print(f"✔️ Saved {len(self.pending_messages)} pending messages to '{self.PENDING_MESSAGES_PATH}'.")
            else:
                # Clear the file if there are no pending messages
                open(self.PENDING_MESSAGES_PATH, 'w').close()
                print("✔️ Cleared pending messages file.")
        except Exception as e:
            print(f"❌ Failed to save pending messages: {e}")

    def load_pending_messages(self):
        """Loads pending messages from a file, if available."""
        try:
            with open(self.PENDING_MESSAGES_PATH, 'r', encoding='utf-8') as f:
                return [json.loads(line.strip()) for line in f.readlines()]
        except FileNotFoundError:
            print("No pending messages file found, starting fresh.")
            return []
        except Exception as e:
            print(f"❌ Failed to load pending messages: {e}")
            return []

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
                    f.write("\n")
            print(f"✔️ Final blockchain saved to {self.FINAL_BLOCKCHAIN_PATH}")
        except Exception as e:
            print(f"❌ Failed to save final blockchain: {e}")
