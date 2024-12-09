import hashlib
import os
import time

# Ensure the data folder exists
DATA_DIR = 'data'
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
    
    def get_message_requirement(self):
        """Calculates the number of messages required to mine the next block."""
        block_index = len(self.chain)
        if block_index == 0:
            return 1
        phase = (block_index - 1) // 3
        return 100 * (2 ** phase)
    
    def add_message(self, message):
        """Adds a new message to the pending messages and checks if a new block can be mined."""
        self.pending_messages.append(message)
        print(f"📥 Added message: '{message}' ({len(self.pending_messages)}/{self.get_message_requirement()} required)")
        self.check_mine_block()

    def check_mine_block(self):
        """Checks if the pending messages meet the mining requirement and mines a block if true."""
        messages_needed = self.get_message_requirement()
        if len(self.pending_messages) >= messages_needed:
            self.mine_block()

    def mine_block(self):
        """Mines a new block using the pending messages."""
        previous_block = self.chain[-1]
        messages_needed = self.get_message_requirement()
        block_messages = self.pending_messages[:messages_needed]
        new_block = Block(len(self.chain), block_messages, previous_block.hash)
        self.chain.append(new_block)
        print(f"⛏️ Mined Block {new_block.index} with {len(new_block.messages)} messages!")
        print(f"🔐 Block Hash: {new_block.hash}\n")
        
        self.pending_messages = self.pending_messages[messages_needed:]
        self.save_pending_messages()

    def save_pending_messages(self):
        """Saves all pending messages to a file only if there are pending messages."""
        if self.pending_messages:  # Save only if there are messages to save
            with open(self.PENDING_MESSAGES_PATH, 'w', encoding='utf-8') as f:
                for message in self.pending_messages:
                    f.write(message + "\n")
            print(f"💾 Saved {len(self.pending_messages)} pending messages to '{self.PENDING_MESSAGES_PATH}'.")

    def load_pending_messages(self):
        """Loads pending messages from a file, if available."""
        try:
            with open(self.PENDING_MESSAGES_PATH, 'r', encoding='utf-8') as f:
                messages = [line.strip() for line in f.readlines()]
            print("")
            print(f"📂 Loaded {len(messages)} pending messages from '{self.PENDING_MESSAGES_PATH}'.")
            return messages
        except FileNotFoundError:
            print(f"📂 No partially mined block found in '{self.PENDING_MESSAGES_PATH}' (starting fresh).")
            return []

    def save_final_blockchain(self):
        """Saves the full blockchain to a file."""
        with open(self.FINAL_BLOCKCHAIN_PATH, 'w', encoding='utf-8') as f:
            for block in self.chain:
                f.write(f"🔗 Block {block.index}:\n")
                f.write(f"  Timestamp: {time.ctime(block.timestamp)}\n")
                f.write(f"  Messages ({len(block.messages)} total): {block.messages}\n")
                f.write(f"  Previous Hash: {block.previous_hash}\n")
                f.write(f"  Hash: {block.hash}\n\n")
        print(f"💾 Saved final blockchain to '{self.FINAL_BLOCKCHAIN_PATH}'.")
