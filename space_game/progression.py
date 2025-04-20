import json
import os

PROGRESSION_FILE = 'progression.json'


def load_progression():
    """Load progression from a JSON file. If file doesn't exist, return default progression."""
    if os.path.exists(PROGRESSION_FILE):
        try:
            with open(PROGRESSION_FILE, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print("Error loading progression:", e)
    # Default progression if file doesn't exist or error occurs
    return {"level": 1, "xp": 0, "high_score": 0}


def save_progression(progression):
    """Save the progression dictionary to a JSON file."""
    try:
        with open(PROGRESSION_FILE, 'w') as f:
            json.dump(progression, f)
    except Exception as e:
        print("Error saving progression:", e)


def update_progression(score, xp_gain, progression):
    """Update progression by adding xp_gain, update high score, and perform level up if xp threshold reached."""
    # Update high score
    if score > progression.get("high_score", 0):
        progression["high_score"] = score
    
    # Add XP
    progression["xp"] = progression.get("xp", 0) + xp_gain
    
    # Level up: Let's define level up threshold as level * 100 xp
    while progression["xp"] >= progression["level"] * 100:
        progression["xp"] -= progression["level"] * 100
        progression["level"] += 1
        print(f"Leveled up! New level: {progression['level']}")
    
    save_progression(progression)
    return progression 