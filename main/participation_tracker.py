from collections import defaultdict

# Participation tracker
default_participation = lambda: defaultdict(int)
participation_tracker = defaultdict(default_participation)

def update_participation(user, block_index):
    """
    Updates the participation tracker for a user.
    """
    participation_tracker[user][block_index] += 1

def calculate_participation_percentage(user, total_blocks_chain):
    """
    Calculates the percentage of blocks the user has participated in.
    """
    total_blocks = len(participation_tracker[user])
    if total_blocks == 0:
        return 0.0
    return (total_blocks / total_blocks_chain) * 100

def get_participation_data():
    """
    Retrieves all participation data.
    """
    return participation_tracker
