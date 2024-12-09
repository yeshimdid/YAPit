import hashlib  # For hashing (fingerprints)
import os  # For file operations

# Ensure the data folder exists
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

class Block:
    """Represents a single block in the blockchain."""
    def __init__(self, index, messages, previous_hash):
        self.index = index
        self.messages = messages
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculates the hash of the block's contents."""
        block_content = f"{self.index}{''.join(self.messages)}{self.previous_hash}"
        return hashlib.sha256(block_content.encode()).hexdigest()


class Blockchain:
    """Manages the entire blockchain and message handling logic."""
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_messages = self.load_pending_messages()
        self.save_final_blockchain()  # Save blockchain state at startup
    
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
        if not message.strip():  # Prevent empty messages
            print("⚠️ Message cannot be blank.")
            return
        
        self.pending_messages.append(message)
        self.save_pending_messages()
        messages_needed = self.get_message_requirement()
        print(f"📥 Added message: '{message}' ({len(self.pending_messages)}/{messages_needed} required)")
        
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
        
        self.pending_messages = self.pending_messages[messages_needed:]  # Remove used messages
        self.save_pending_messages()
        self.save_final_blockchain()
    
    def save_pending_messages(self):
        """Saves all pending messages to a file in the /data directory."""
        try:
            pending_path = os.path.join(DATA_DIR, 'pending_messages.txt')
            with open(pending_path, 'w', encoding='utf-8') as f:
                for message in self.pending_messages:
                    f.write(message + "\n")
            print(f"💾 Saved {len(self.pending_messages)} pending messages to '{pending_path}'.")
        except Exception as e:
            print(f"❌ Error saving pending messages: {e}")
    
    def load_pending_messages(self):
        """Loads pending messages from the /data directory, if available."""
        try:
            pending_path = os.path.join(DATA_DIR, 'pending_messages.txt')
            with open(pending_path, 'r', encoding='utf-8') as f:
                messages = [line.strip() for line in f.readlines()]
            print("")
            print(f"📂 Loaded {len(messages)} pending messages from '{pending_path}'.")
            return messages
        except FileNotFoundError:
            print(f"📂 No partially mined block found in '{DATA_DIR}' (starting fresh).")
            return []
        except Exception as e:
            print(f"❌ Error loading pending messages: {e}")
            return []
    
    def save_final_blockchain(self):
        """Saves the full blockchain to a file in the /data directory."""
        try:
            blockchain_path = os.path.join(DATA_DIR, 'final_blockchain.txt')
            with open(blockchain_path, 'w', encoding='utf-8') as f:
                for block in self.chain:
                    f.write(f"🔗 Block {block.index}:\n")
                    f.write(f"  Messages ({len(block.messages)} total): {block.messages}\n")
                    f.write(f"  Previous Hash: {block.previous_hash}\n")
                    f.write(f"  Hash: {block.hash}\n\n")
            print(f"💾 Saved final blockchain to '{blockchain_path}'.")
        except Exception as e:
            print(f"❌ Error saving blockchain: {e}")
