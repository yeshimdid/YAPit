from collections import defaultdict
import os

DATA_DIR = '../vip'
PARTICIPATION_STATS_PATH = os.path.join(DATA_DIR, 'participation_stats.txt')
os.makedirs(DATA_DIR, exist_ok=True)

# Participation tracker
default_participation = lambda: defaultdict(int)
participation_tracker = defaultdict(default_participation)

def update_participation(user, block_index):
    """
    Updates the participation tracker for a user.
    """
    participation_tracker[user][block_index] += 1
    save_participation_stats()

def calculate_participation_percentage(user, total_blocks_chain):
    """
    Calculates the percentage of blocks the user has participated in.
    """
    total_blocks = len(participation_tracker[user])
    if total_blocks == 0:
        return 0.0
    return (total_blocks / total_blocks_chain) * 100

def calculate_current_block_contribution(user, current_block_index):
    """
    Calculates the percentage of contributions a user has made to the current block being mined.
    """
    # Total contributions to the current block by all users
    total_contributions_to_current_block = sum(
        blocks[current_block_index] for blocks in participation_tracker.values()
    )
    if total_contributions_to_current_block == 0:
        return 0.0
    # Contributions by this user to the current block
    current_block_contributions = participation_tracker[user][current_block_index]
    return (current_block_contributions / total_contributions_to_current_block) * 100

def get_participation_data():
    """
    Retrieves all participation data.
    """
    return participation_tracker

def save_participation_stats():
    """
    Saves the current participation statistics to a file.
    """
    try:
        with open(PARTICIPATION_STATS_PATH, 'w', encoding='utf-8') as f:
            f.write("User Participation Statistics:\n")
            for user, blocks in participation_tracker.items():
                total_blocks = len(blocks)
                f.write(f"User: {user}\n")
                f.write(f"Total Blocks Contributed To: {total_blocks}\n")
                f.write(f"Block Indices: {list(blocks.keys())}\n")
                # Calculate current block contribution
                if blocks:
                    current_block_index = max(blocks.keys())  # Assume latest block index is current
                    current_contribution = calculate_current_block_contribution(user, current_block_index)
                    f.write(f"Current Block Contribution: {current_contribution:.2f}%\n")
                f.write("\n")
        print(f"✔️ Participation statistics saved to {PARTICIPATION_STATS_PATH}")
    except Exception as e:
        print(f"Failed to save participation statistics: {e}")
