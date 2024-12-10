import json
import os

DATA_DIR = '../vip'
USER_DATA_PATH = os.path.join(DATA_DIR, 'users.json')

def migrate_users_file():
    try:
        with open(USER_DATA_PATH, 'r', encoding='utf-8') as f:
            users = json.load(f)
        migrated_users = {}
        for username, details in users.items():
            if isinstance(details, str):  # Assume old format
                migrated_users[username] = {
                    "password": details,
                    "wallet": "unknown",  # Placeholder, replace with actual wallets if known
                    "email": "unknown@example.com"  # Placeholder, replace with actual emails if known
                }
            else:
                migrated_users[username] = details
        with open(USER_DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(migrated_users, f, indent=4)
        print("✔️ User data migrated successfully.")
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    migrate_users_file()
