import hashlib  # For hashing (fingerprints)
import os  # For file operations

class Block:
    def __init__(self, index, messages, previous_hash):
        self.index = index
        self.messages = messages
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_content = f"{self.index}{''.join(self.messages)}{self.previous_hash}"
        return hashlib.sha256(block_content.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_messages = self.load_pending_messages()
        self.save_final_blockchain()  # Save blockchain state at startup
    
    def create_genesis_block(self):
        return Block(0, ["Genesis Block"], "0")
    
    def get_message_requirement(self):
        block_index = len(self.chain)
        if block_index == 0:
            return 1
        phase = (block_index - 1) // 3
        return 100 * (2 ** phase)
    
    def add_message(self, message):
        self.pending_messages.append(message)
        self.save_pending_messages()
        messages_needed = self.get_message_requirement()
        print(f"📥 Added message: '{message}' ({len(self.pending_messages)}/{messages_needed} required)")
        
        if len(self.pending_messages) >= messages_needed:
            self.mine_block()
    
    def mine_block(self):
        previous_block = self.chain[-1]
        messages_needed = self.get_message_requirement()
        block_messages = self.pending_messages[:messages_needed]
        new_block = Block(len(self.chain), block_messages, previous_block.hash)
        self.chain.append(new_block)
        print(f"⛏️ Mined Block {new_block.index} with {len(new_block.messages)} messages!")
        print(f"🔐 Block Hash: {new_block.hash}\n")
        self.pending_messages = self.pending_messages[messages_needed:]
        self.save_pending_messages()
        self.save_final_blockchain()
    
    def save_pending_messages(self):
        with open('pending_messages.txt', 'w', encoding='utf-8') as f:  # ✅ UTF-8 encoding added here
            for message in self.pending_messages:
                f.write(message + "\n")
        print(f"💾 Saved {len(self.pending_messages)} pending messages to 'pending_messages.txt'.")
    
    def load_pending_messages(self):
        if os.path.exists('pending_messages.txt'):
            with open('pending_messages.txt', 'r', encoding='utf-8') as f:  # ✅ UTF-8 encoding added here
                messages = [line.strip() for line in f.readlines()]
            print("")
            print(f"📂 Loaded {len(messages)} pending messages from 'pending_messages.txt'.")
            return messages
        else:
            print("📂 No partially mined block found (starting fresh).")
            return []
    
    def save_final_blockchain(self):
        """Save the entire blockchain to a file."""
        with open('final_blockchain.txt', 'w', encoding='utf-8') as f:  # ✅ UTF-8 encoding added here
            for block in self.chain:
                f.write(f"🔗 Block {block.index}:\n")
                f.write(f"  Messages ({len(block.messages)} total): {block.messages}\n")
                f.write(f"  Previous Hash: {block.previous_hash}\n")
                f.write(f"  Hash: {block.hash}\n\n")
        print(f"💾 Saved final blockchain to 'final_blockchain.txt'.")
    

blockchain = Blockchain()

print("")
print("💬 Welcome to YapIt!")
print("")
print("The blockchain built by interaction.")
print("")
print("For you, by you")
print("")
print("Type a message to add it to the blockchain.")
print("Type 'exit' to disconnect from the blockchain")

while True:
    message = input("📝 Your message: ")
    if message.lower() == 'exit':
        blockchain.save_final_blockchain()
        print("\n🔗 Final blockchain has been saved to 'final_blockchain.txt'.")
        break
    blockchain.add_message(message)
