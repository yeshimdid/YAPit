import hashlib
import os
import time
import json
from participation_tracker import update_participation, save_participation_stats, load_participation_stats

# Sets up the directory for storing data files
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
    CURRENT_BLOCK_PATH = os.path.join(DATA_DIR, 'current_block.txt')

    def __init__(self):
        load_participation_stats()
        self.chain = [self.create_genesis_block()]
        self.pending_messages = self.load_pending_messages()
        self.current_block_index = self.load_current_block_index()
        print(f"Blockchain initialized with {len(self.chain)} blocks.")

    def create_genesis_block(self):
        """Creates the first block (Genesis block) in the blockchain."""
        return Block(0, ["Genesis Block"], "0")

    def save_current_block_index(self):
        """Saves the current block index to a file."""
        try:
            with open(self.CURRENT_BLOCK_PATH, 'w', encoding='utf-8') as f:
                f.write(str(self.current_block_index))
            print(f"✔️ Current block index saved as {self.current_block_index}.")
        except Exception as e:
            print(f"❌ Failed to save current block index: {e}")

    def load_current_block_index(self):
        """Loads the current block index from a file, or defaults to the latest mined block."""
        try:
            with open(self.CURRENT_BLOCK_PATH, 'r', encoding='utf-8') as f:
                return int(f.read().strip())
        except FileNotFoundError:
            print("No current block index file found. Starting at latest mined block.")
            return len(self.chain) - 1
        except Exception as e:
            print(f"❌ Failed to load current block index: {e}")
            return len(self.chain) - 1

    def add_message(self, username, message):
        """Adds a new message to the pending messages with the user's username."""
        self.pending_messages.append({"username": username, "message": message})
        update_participation(username, self.current_block_index)
        self.check_mine_block()
        self.save_pending_messages()

    def check_mine_block(self):
        """Checks if the pending messages meet the mining requirement and mines a block if true."""
        messages_needed = self.get_message_requirement()
        if len(self.pending_messages) >= messages_needed:
            self.mine_block()

    def get_message_requirement(self):
        """Calculates the number of messages required to mine the next block."""
        block_index = self.current_block_index + 1
        return 100 * (2 ** ((block_index - 1) // 3))

    def mine_block(self):
        """Mines a new block using the pending messages."""
        previous_block = self.chain[-1]
        messages_needed = self.get_message_requirement()
        messages = [msg["message"] for msg in self.pending_messages[:messages_needed]]
        new_block = Block(len(self.chain), messages, previous_block.hash)
        self.chain.append(new_block)
        print(f"Mined new block: {new_block.hash}")

        # Advance to the next block
        self.current_block_index += 1
        self.save_current_block_index()

        # Remove mined messages and save state
        self.pending_messages = self.pending_messages[messages_needed:]
        save_participation_stats()
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
