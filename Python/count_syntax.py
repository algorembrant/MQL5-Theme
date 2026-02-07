import re
import os

def count_syntax_items(filepath):
    """Counts syntax items in a markdown file with specific format."""
    count = 0
    
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        in_code_block = False
        for line in f:
            line = line.strip()
            
            if line.startswith('```'):
                in_code_block = not in_code_block
                continue
            
            if in_code_block:
                # Split by whitespace to get items
                items = line.split()
                count += len(items)
                
    print(f"Total syntax items in {os.path.basename(filepath)}: {count}")

if __name__ == "__main__":
    # Adjust path as needed
    target_file = r"c:\Users\User\Desktop\VSCode\MQL5-Theme\syntax.md"
    count_syntax_items(target_file)
