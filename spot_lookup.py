import json
import os
import re

FILENAME = "spots.json"

def load_spots():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_spots(spots):
    with open(FILENAME, "w") as f:
        json.dump(spots, f, indent=2)
        print(f"✅ Saved {len(spots)} spots to {FILENAME}.")

def extract_name_and_id_from_url(url):
    """
    Extract the spot name and ID from the given Surfline URL.

    Args:
        url (str): The Surfline URL.

    Returns:
        tuple: A tuple containing the spot name and spot ID.
    """
    match = re.match(r"https://www\.surfline\.com/surf-report/([^/]+)/([^/]+)", url)
    if match:
        spot_name = match.group(1)  # Extract the spot name
        spot_id = match.group(2)    # Extract the spot ID
        return spot_name, spot_id
    else:
        raise ValueError("Invalid Surfline URL format.")

def main():
    spots = load_spots()
    
    while True:
        print("\nEnter new surf spot info (or type 'q' to quit):")
        url = input("  Spot URL: ").strip()
        if url.lower() == 'q':
            break

        # Check if the URL already exists in the spots list
        if any(spot["url"] == url for spot in spots):
            print("⚠️ This spot is already in the list. Skipping...")
            continue

        try:
            # Extract the spot name and ID from the URL
            spot_name, spot_id = extract_name_and_id_from_url(url)
        except ValueError as e:
            print(f"Error: {e}")
            continue

        new_spot = {
            "name": spot_name,
            "spotId": spot_id,
            "url": url
        }

        spots.append(new_spot)
        save_spots(spots)

if __name__ == "__main__":
    main()
