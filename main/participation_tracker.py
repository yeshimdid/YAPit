import hashlib
import os
import json
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

PARTICIPATION_STATS_PATH = os.path.join(DATA_DIR, 'participation_stats.json')

# Initialize participation tracker
participation_tracker = defaultdict(lambda: defaultdict(int))

def load_participation_stats():
    try:
        with open(PARTICIPATION_STATS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for user, blocks in data.items():
                for block_index, details in blocks.items():
                    participation_tracker[user][int(block_index)] += details["count"]
        print("✔️ Participation statistics loaded and merged.")
    except FileNotFoundError:
        print("No participation stats file found. Starting fresh.")
    except Exception as e:
        print(f"❌ Failed to load participation stats: {e}")

def save_participation_stats():
    try:
        total_contributions_per_block = defaultdict(int)
        for blocks in participation_tracker.values():
            for block_index, count in blocks.items():
                total_contributions_per_block[block_index] += count

        participation_stats_with_percentages = {
            user: {
                block_index: {
                    "count": count,
                    "percentage": (count / total_contributions_per_block[block_index]) * 100
                }
                for block_index, count in blocks.items()
            }
            for user, blocks in participation_tracker.items()
        }

        with open(PARTICIPATION_STATS_PATH, 'w', encoding='utf-8') as f:
            json.dump(participation_stats_with_percentages, f, indent=4)
        print(f"✔️ Participation statistics saved to {PARTICIPATION_STATS_PATH}")
    except Exception as e:
        print(f"❌ Failed to save participation statistics: {e}")

def update_participation(user, block_index):
    participation_tracker[user][block_index] += 1
    save_participation_stats()
