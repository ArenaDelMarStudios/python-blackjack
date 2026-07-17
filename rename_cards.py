import os

# Path to your cards folder (change this if your folder has a different path)
CARDS_DIR = "cards"

# Mappings for ranks and suits
RANK_MAP = {
    "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "10": "10",
    "jack": "J",
    "queen": "Q",
    "king": "K",
    "ace": "A"
}

SUIT_MAP = {
    "clubs": "C",
    "diamonds": "D",
    "hearts": "H",
    "spades": "S"
}

def rename_cards():
    if not os.path.exists(CARDS_DIR):
        print(f"Error: Folder '{CARDS_DIR}' not found. Please place this script next to your cards folder.")
        return

    renamed_count = 0
    files = os.listdir(CARDS_DIR)

    for filename in files:
        # We only want to rename files, skipping system files like .DS_Store
        if not os.path.isfile(os.path.join(CARDS_DIR, filename)):
            continue

        # Split file into name and extension (e.g., "king_of_spades" and ".png")
        name, ext = os.path.splitext(filename)
        name_lower = name.lower()

        # Check if the filename fits the "rank_of_suit" pattern
        if "_of_" in name_lower:
            parts = name_lower.split("_of_")
            if len(parts) == 2:
                raw_rank, raw_suit = parts[0], parts[1]

                # Map to the new shorthand names if they match our dictionary keys
                if raw_rank in RANK_MAP and raw_suit in SUIT_MAP:
                    new_name = f"{RANK_MAP[raw_rank]}{SUIT_MAP[raw_suit]}{ext}"
                    
                    old_path = os.path.join(CARDS_DIR, filename)
                    new_path = os.path.join(CARDS_DIR, new_name)

                    try:
                        os.rename(old_path, new_path)
                        print(f"Renamed: {filename} ➔ {new_name}")
                        renamed_count += 1
                    except Exception as e:
                        print(f"Failed to rename {filename}: {e}")

    print(f"\nFinished! Successfully renamed {renamed_count} files.")

if __name__ == "__main__":
    rename_cards()