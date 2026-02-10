"""
Script to parse mql5.md and extract all CAPSLOCK_NAMES_SYNTAX identifiers.
These are identifiers that:
- Are ALL CAPS
- Have at least one underscore '_' between words
- Examples: SYMBOL_TRADE_MODE, ACCOUNT_INFO_INTEGER, OBJ_ARROW_UP
"""

import re
from pathlib import Path
from collections import defaultdict

def extract_capslock_syntax(filepath: str) -> set:
    """
    Extract all CAPSLOCK_NAMES_SYNTAX identifiers from a file.
    
    Pattern: All uppercase letters with underscores, at least one underscore required.
    Must have letters on both sides of underscore(s).
    """
    # Pattern explanation:
    # - [A-Z][A-Z0-9]* : Start with uppercase letter, followed by optional uppercase letters or digits
    # - (_[A-Z0-9]+)+ : One or more groups of underscore followed by uppercase letters/digits
    pattern = r'\b[A-Z][A-Z0-9]*(_[A-Z0-9]+)+\b'
    
    identifiers = set()
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    matches = re.findall(pattern, content)
    # findall with groups returns only the last group, so we need to use finditer
    for match in re.finditer(pattern, content):
        identifiers.add(match.group())
    
    return identifiers


def categorize_identifiers(identifiers: set) -> dict:
    """
    Categorize identifiers by their prefix (first part before underscore).
    """
    categories = defaultdict(list)
    
    for identifier in sorted(identifiers):
        # Get the prefix (first part before underscore)
        parts = identifier.split('_')
        prefix = parts[0]
        categories[prefix].append(identifier)
    
    return dict(sorted(categories.items()))


def generate_markdown(categories: dict, output_path: str):
    """
    Generate a markdown file with categorized identifiers.
    """
    total_count = sum(len(items) for items in categories.values())
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# MQL5 CAPSLOCK_NAMES_SYNTAX Identifiers\n\n")
        f.write(f"**Total identifiers found:** {total_count}\n\n")
        f.write(f"**Total categories:** {len(categories)}\n\n")
        f.write("---\n\n")
        f.write("## Table of Contents\n\n")
        
        # Generate TOC
        for prefix in categories.keys():
            count = len(categories[prefix])
            f.write(f"- [{prefix}_* ({count} items)](#{prefix.lower()})\n")
        
        f.write("\n---\n\n")
        
        # Generate content for each category
        for prefix, items in categories.items():
            f.write(f"## {prefix}_* <a name=\"{prefix.lower()}\"></a>\n\n")
            f.write(f"*{len(items)} identifiers*\n\n")
            f.write("```\n")
            for item in sorted(items):
                f.write(f"{item}\n")
            f.write("```\n\n")
    
    return total_count, len(categories)


def main():
    # Paths
    input_file = Path(__file__).parent / "mql5.md"
    output_file = Path(__file__).parent / "mql5_capslock_syntax.md"
    
    print(f"Reading from: {input_file}")
    
    # Extract identifiers
    identifiers = extract_capslock_syntax(input_file)
    print(f"Found {len(identifiers)} unique CAPSLOCK_NAMES_SYNTAX identifiers")
    
    # Categorize by prefix
    categories = categorize_identifiers(identifiers)
    print(f"Categorized into {len(categories)} prefix groups")
    
    # Generate markdown output
    total, cat_count = generate_markdown(categories, output_file)
    
    print(f"\nOutput written to: {output_file}")
    print(f"Total identifiers: {total}")
    print(f"Total categories: {cat_count}")


if __name__ == "__main__":
    main()
