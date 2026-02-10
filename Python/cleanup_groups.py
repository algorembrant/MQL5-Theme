import re

def clean_line(line):
    """Clean a line by removing artifacts and checking if it's valid syntax."""
    # Remove carriage return and newline
    line = line.rstrip('\r\n')
    
    # Skip empty lines
    if not line.strip():
        return None
    
    # Skip lines that are mostly dots (page number references)
    if re.match(r'^[\s\.]*\d+$', line.strip()) or '..' in line:
        return None
    
    # Skip copyright notices
    if '© 2000-2025' in line or 'MetaQuotes' in line:
        return None
    
    # Skip page break characters (form feed)
    if line.strip().startswith('\f') or re.match(r'^\x0c?\d+$', line.strip()):
        return None
    
    # Skip "Content" header
    if line.strip() == 'Content':
        return None
    
    # Keep group tags
    if line.strip() == '<group>' or line.strip() == '</group>':
        return line.strip()
    
    # Keep the line if it's a valid syntax item (non-empty after cleaning)
    cleaned = line.strip()
    if cleaned:
        return cleaned
    
    return None

def process_file(input_path, output_path, start_line=1238):
    """Process the file starting from start_line."""
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Keep lines 1-1237 as-is
    output_lines = lines[:start_line-1]
    
    # Process remaining lines
    in_group = False
    current_group = []
    
    for i, line in enumerate(lines[start_line-1:], start=start_line):
        cleaned = clean_line(line)
        
        if cleaned is None:
            continue
        
        if cleaned == '<group>':
            in_group = True
            current_group = ['<group>\r\n']
        elif cleaned == '</group>':
            if in_group and len(current_group) > 1:  # Only add group if it has content
                current_group.append('</group>\r\n')
                current_group.append('\r\n')  # Empty line after group
                output_lines.extend(current_group)
            in_group = False
            current_group = []
        elif in_group:
            current_group.append(cleaned + '\r\n')
        else:
            # Not in a group, but might be standalone syntax - skip these noise items
            pass
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    print(f"Processed {len(lines)} lines, output has {len(output_lines)} lines")
    print(f"Saved to {output_path}")

if __name__ == '__main__':
    input_file = r'c:\Users\User\Desktop\VSCode\MQL5-Theme\mql5 copy.md'
    output_file = r'c:\Users\User\Desktop\VSCode\MQL5-Theme\mql5 copy.md'  # Overwrite original
    process_file(input_file, output_file)
