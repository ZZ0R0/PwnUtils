#!/usr/bin/env python3
# filepath: /share/utils/count.py

import sys

def count_chars():
    # Skip the script name (sys.argv[0])
    args = sys.argv[1:]
    
    if not args:
        print("Usage: count.py <string1> [string2] [string3] ...")
        print("Example: count.py hello world")
        return
    
    # Count characters in all arguments
    total_chars = sum(len(arg) for arg in args)
    print(total_chars)

if __name__ == "__main__":
    count_chars()