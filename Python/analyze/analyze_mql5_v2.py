
import re
import sys

file_path = r"c:\Users\User\Desktop\VSCode\MQL5-Theme\mql5.md"

try:
    unique_matches = set()
    unique_matches_caps = set()

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Pattern 1: Starts with Inp
            matches = re.findall(r"\bInp[a-zA-Z0-9_]+", line)
            unique_matches.update(matches)

            # Pattern 2: Starts with INP
            matches_caps = re.findall(r"\bINP_[a-zA-Z0-9_]+", line)
            unique_matches_caps.update(matches_caps)
            
            # Also check for ALL CAPS starting with INP (e.g. INP_SOMETHING)
            # The previous regex \bINP_\w+ covers INP_SOMETHING
            # But what if it is INPSOMETHING? (Less likely for constants)
            
    print(f"Found {len(unique_matches)} unique matches starting with 'Inp'.")
    print("First 20 'Inp' matches:")
    for m in sorted(list(unique_matches))[:20]:
        print(m)

    print(f"\nFound {len(unique_matches_caps)} unique matches starting with 'INP_'.")
    print("First 20 'INP_' matches:")
    for m in sorted(list(unique_matches_caps))[:20]:
        print(m)

except Exception as e:
    print(f"Error: {e}")
