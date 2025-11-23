from datetime import datetime
import os

# Feature: Added 5-minute wait time rule

class DuplicateVisitorError(Exception):
    pass

class EarlyEntryError(Exception):
    pass

FILENAME = "visitors.txt"

def ensure_file():
    """Create the visitors file if it doesn't exist"""
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f:
            pass  # Create empty file

def get_last_visitor():
    """
    Returns a tuple: (name, datetime_object) of the last visitor
    Returns None if file is empty
    """
    if not os.path.exists(FILENAME):
        return None
    
    with open(FILENAME, "r") as f:
        lines = f.readlines()
    
    if not lines:
        return None
    
    # Get the last line
    last_line = lines[-1].strip()
    
    # Parse it: format is "Name | 2024-01-01T12:00:00"
    parts = last_line.split(" | ")
    name = parts[0]
    timestamp_str = parts[1]
    timestamp = datetime.fromisoformat(timestamp_str)
    
    return (name, timestamp)

def add_visitor(visitor_name):
    """
    Add a visitor to the log file
    Raises DuplicateVisitorError if same person tries to enter twice
    Raises EarlyEntryError if less than 5 minutes since last visitor
    """
    last_visitor = get_last_visitor()
    
    if last_visitor:
        last_name, last_time = last_visitor
        
        # Check for duplicate consecutive visitor
        if last_name == visitor_name:
            raise DuplicateVisitorError(f"{visitor_name} just entered. Cannot enter twice in a row.")
        
        # Check if 5 minutes have passed
        time_diff = datetime.now() - last_time
        if time_diff.total_seconds() < 300:  # 300 seconds = 5 minutes
            raise EarlyEntryError(f"Please wait 5 minutes between visitors. Only {time_diff.total_seconds()/60:.1f} minutes have passed.")
    
    # Add the visitor
    with open(FILENAME, "a") as f:
        f.write(f"{visitor_name} | {datetime.now().isoformat()}\n")

def main():
    ensure_file()
    name = input("Enter visitor's name: ")
    try:
        add_visitor(name)
        print("Visitor added successfully!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()