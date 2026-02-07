import re
import os

def load_syntax_md(filepath):
    """Parses syntax.md to get existing categories and items."""
    categories = {}
    current_category = None
    
    if not os.path.exists(filepath):
        return categories

    with open(filepath, 'r', encoding='utf-8') as f:
        # Simple parsing for categories
        for line in f:
            line = line.strip()
            if line.startswith('## '):
                match = re.search(r'##\s+(.*)', line)
                if match:
                    current_category = match.group(1).strip()
                    categories[current_category] = set()
            elif current_category and line and not line.startswith('```') and not line.startswith('---') and not line.startswith('#'):
                 # syntax.md style: items separated by double spaces or single space
                items = re.split(r'\s+', line)
                for item in items:
                    if item:
                         categories[current_category].add(item)
    return categories

def extract_from_mores_md(filepath):
    """Extracts syntax items from mores.md."""
    items = set()
    
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return items

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find code blocks
    code_blocks = re.findall(r'```mql5\n(.*?)\n```', content, re.DOTALL)

    for block in code_blocks:
        # Normalize whitespace
        block_clean = ' '.join(block.split())
        
        # 1. Structs: struct Name
        struct_match = re.search(r'\bstruct\s+(\w+)', block_clean)
        if struct_match:
            items.add(struct_match.group(1))

        # 2. Enums: enum Name
        enum_match = re.search(r'\benum\s+(\w+)', block_clean)
        if enum_match:
            items.add(enum_match.group(1))

        # 3. Unions: union Name
        union_match = re.search(r'\bunion\s+(\w+)', block_clean)
        if union_match:
            items.add(union_match.group(1))

        # 4. Classes: class Name
        class_match = re.search(r'\bclass\s+(\w+)', block_clean)
        if class_match:
            items.add(class_match.group(1))
            
        # 5. Functions:  Type Name(...)
        # Heuristic: <word> <Name> (
        # We look for a pattern where a word is followed by a '('
        # And that word is likely permitted to be a function name.
        
        # find all words followed by (
        candidates = re.finditer(r'(\w+)\s*\(', block_clean)
        for cand in candidates:
            name = cand.group(1)
            # Filter keywords
            if name not in ['if', 'while', 'for', 'switch', 'return', 'sizeof']:
                 # Also filter if previous word was 'new' or 'delete' (unlikely in definitions)
                 items.add(name)

    return items

def categorize_items(existing_categories, new_items):
    """Categorizes items."""
    
    # Init new category map with existing items
    # We want to keep the structure of syntax.md
    final_categories = {k: list(v) for k, v in existing_categories.items()}
    
    # We also want to capture items that were in syntax.md but potentially not in mores.md?
    # Or just use syntax.md as the base classification system.
    
    # Flatten existing items for quick lookup
    existing_items_flat = set()
    for cat_items in final_categories.values():
        existing_items_flat.update(cat_items)

    # Heuristic mapping for new items
    heuristics = {
        'Array Functions': r'^Array',
        'String Functions': r'^String',
        'Math Functions': r'^Math',
        'Object Functions': r'^Object',
        'File Functions': r'^File',
        'Account Info Functions': r'^Account',
        'Check Functions': r'^Check',
        'Event Handler Functions': r'^On',
        'Market Info Functions': r'^Symbol',
        'Common Functions': r'^(Print|Alert|Comment|Send|Sleep|Get)',
        'Conversion Functions': r'^(Char|Double|Integer|Time|Color|Enum)To',
        'Indicator Functions': r'^i[A-Z]',
        'Trade Functions': r'^(Order|Position|History|Deal)',
        'Standard Library Classes': r'^C[A-Z]',
        'MQL5 Structures': r'^Mql',
        'Chart Functions': r'^Chart',
        'Text Functions': r'^Text',
        'Date and Time': r'^Time',
        'Global Variables': r'^Global',
        'Custom Indicators': r'^Indicator',
        'Signal Functions': r'^Signal',
    }

    uncategorized = []

    for item in new_items:
        if item in existing_items_flat:
            continue
            
        placed = False
        for cat, regex in heuristics.items():
            if re.search(regex, item):
                if cat not in final_categories:
                    final_categories[cat] = []
                if item not in final_categories[cat]:
                    final_categories[cat].append(item)
                placed = True
                break
        
        if not placed:
            uncategorized.append(item)
            
    if uncategorized:
        if "Uncategorized" not in final_categories:
            final_categories["Uncategorized"] = []
        final_categories["Uncategorized"].extend(uncategorized)
        
    return final_categories

def write_moress_md(categories, output_filepath):
    """Writes the content to moress.md."""
    
    # Simple sort of categories: default ones first (if we knew order), or just alphabetical
    # We'll rely on insertion order from the load_syntax_md if possible, appending new ones.
    
    with open(output_filepath, 'w', encoding='utf-8') as f:
        # Write header matching syntax.md style or close to it
        f.write("# MQL5 Syntax Reference\n\n")
        f.write("Generated from `mores.md`.\n\n")
        f.write("---\n\n")

        for cat, items in categories.items():
            if not items:
                continue
            
            f.write(f"## {cat}\n")
            f.write("```\n")
            
            # Sort items alpha
            sorted_items = sorted(list(items))
            
            # Write items, word wrapped
            line_buf = ""
            for item in sorted_items:
                if len(line_buf) + len(item) + 2 > 80:
                    f.write(line_buf.strip() + "\n")
                    line_buf = item + "  "
                else:
                    line_buf += item + "  "
            
            if line_buf:
                f.write(line_buf.strip() + "\n")
                
            f.write("```\n\n")
            
        f.write("---\n")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Adjust path to match where the files are relative to this script
    # User said mores.md and syntax.md are in c:\Users\User\Desktop\VSCode\MQL5-Theme
    # This script is in c:\Users\User\Desktop\VSCode\MQL5-Theme\Python
    
    # So we go up one level
    project_root = os.path.dirname(base_dir)
    
    syntax_path = os.path.join(project_root, "syntax.md")
    mores_path = os.path.join(project_root, "mores.md")
    output_path = os.path.join(project_root, "moress.md")
    
    print(f"Reading from {syntax_path} and {mores_path}...")
    
    categories = load_syntax_md(syntax_path)
    new_items = extract_from_mores_md(mores_path)
    
    print(f"Extracted {len(new_items)} items from mores.md")
    
    final_cats = categorize_items(categories, new_items)
    
    print(f"Writing to {output_path}...")
    write_moress_md(final_cats, output_path)
    print("Done.")

if __name__ == "__main__":
    main()
