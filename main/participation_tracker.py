import hashlib
import os
import json
from collections import defaultdict

# Set up the directory for storing non-Python files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

PARTICIPATION_STATS_PATH = os.path.join(DATA_DIR, 'participation_stats.json')

# Initialize participation tracker
participation_tracker = defaultdict(lambda: defaultdict(int))

def load_participation_stats():
    """
    Loads the participation statistics from a file, if available, and merges them with the current tracker.
    """
    global participation_tracker
    try:
        with open(PARTICIPATION_STATS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Merge loaded data into participation_tracker
            for user, blocks in data.items():
                for block_index, details in blocks.items():
                    participation_tracker[user][int(block_index)] += details["count"]  # Merge counts
        print("✔️ Participation statistics loaded and merged.")
    except FileNotFoundError:
        print("No participation stats file found. Starting fresh.")
    except Exception as e:
        print(f"❌ Failed to load participation stats: {e}")

def save_participation_stats():
    """
    Saves the current participation statistics to a file with contribution percentages.
    """
    try:
        # Compute total contributions per block
        total_contributions_per_block = defaultdict(int)
        for blocks in participation_tracker.values():
            for block_index, count in blocks.items():
                total_contributions_per_block[block_index] += count

        # Prepare the stats with percentages
        participation_stats_with_percentages = {}
        for user, blocks in participation_tracker.items():
            participation_stats_with_percentages[user] = {
                block_index: {
                    "count": count,
                    "percentage": (count / total_contributions_per_block[block_index]) * 100
                }
                for block_index, count in blocks.items()
            }

        # Save the stats to the file
        with open(PARTICIPATION_STATS_PATH, 'w', encoding='utf-8') as f:
            json.dump(participation_stats_with_percentages, f, indent=4)
        print(f"✔️ Participation statistics saved to {PARTICIPATION_STATS_PATH}")
    except Exception as e:
        print(f"❌ Failed to save participation statistics: {e}")

def update_participation(user, block_index):
    """
    Updates the participation tracker for a user.
    """
    participation_tracker[user][block_index] += 1  # Increment the count
    save_participation_stats()  # Save after every update

def calculate_current_block_contribution(user, current_block_index, total_required_interactions):
    """
    Calculates the percentage of contributions a user has made to the current block relative to the total required interactions.
    """
    # Contributions by this user to the current block
    current_contributions = participation_tracker[user][current_block_index]
    return (current_contributions / total_required_interactions) * 100 if total_required_interactions > 0 else 0.0

def get_participation_data():
    """
    Retrieves all participation data.
    """
    return participation_tracker
