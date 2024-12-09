import hashlib  # For hashing (fingerprints)

class Block:
    def __init__(self, index, data, previous_hash):
        """Create a new block."""
        self.index = index  # The position of the block in the chain
        self.data = data  # The chat message
        self.previous_hash = previous_hash  # Link to the previous block
        self.hash = self.calculate_hash()  # The unique fingerprint of this block
    
    def calculate_hash(self):
        """Create a unique hash for this block using its data."""
        block_content = f"{self.index}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_content.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        """Create the blockchain with the first (genesis) block."""
        self.chain = [self.create_genesis_block()]  # Our blockchain is a list of blocks
    
    def create_genesis_block(self):
        """The first block in the chain."""
        return Block(0, "Genesis Block", "0")
    
    def add_block(self, data):
        """Add a new block with chat message data."""
        previous_block = self.chain[-1]  # Get the last block in the chain
        new_block = Block(len(self.chain), data, previous_block.hash)  # Create the new block
        self.chain.append(new_block)  # Add it to the chain
    
    def print_chain(self):
        """Print all blocks in the blockchain."""
        for block in self.chain:
            print(f"Block {block.index}:")
            print(f"Data: {block.data}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}\n")

# Real-time interactive chat
blockchain = Blockchain()  # Create a blockchain

print("")
print("💬 Welcome to YAPit! A blockchain built by interaction. For you, by you.")
print("")
print(">Type a message to add it to the blockchain.")
print(">Type 'exit' to end the chat and print the final blockchain.\n")

while True:
    message = input("📝 Your message: ")  # Get input from the user
    if message.lower() == 'exit':  # If the user types 'exit', end the chatexit
        print("\n🔗 Here's your final blockchain:")
        blockchain.print_chain()
        break  # Stop the program
    blockchain.add_block(message)  # Add the message to the blockchain
    print(f"✅ Message added to the blockchain!\n")
