
import re

file_path = r"c:\Users\User\Desktop\VSCode\MQL5-Theme\mql5.md"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern 1: Starts with Inp
    # matching Inp followed by word characters
    pattern = r"\bInp\w+"
    matches = re.findall(pattern, content)
    
    # Pattern 2: Starts with INP
    pattern_caps = r"\bINP\w+"
    matches_caps = re.findall(pattern_caps, content)

    unique_matches = sorted(list(set(matches)))
    unique_matches_caps = sorted(list(set(matches_caps)))

    print(f"Found {len(unique_matches)} unique matches starting with 'Inp'.")
    print("First 50 'Inp' matches:")
    for m in unique_matches[:50]:
        print(m)

    print(f"\nFound {len(unique_matches_caps)} unique matches starting with 'INP'.")
    print("First 50 'INP' matches:")
    for m in unique_matches_caps[:50]:
        print(m)

except Exception as e:
    print(f"Error: {e}")
