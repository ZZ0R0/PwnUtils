#!/usr/bin/env python3
# filepath: /share/utils/find.py

import sys

def find_pattern():
    # Check if we have enough arguments
    if len(sys.argv) < 3:
        print("Usage: find.py <string> <pattern>")
        print("Example: find.py abcde cd")
        return
    
    # Get the string and pattern from command line arguments
    string = sys.argv[1]
    pattern = sys.argv[2]
    
    try:
        # Find the offset of the pattern in the string
        offset = string.find(pattern)
        
        if offset == -1:
            print(f"Pattern '{pattern}' not found in '{string}'")
        else:
            print(offset)
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_pattern()