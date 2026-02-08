"""
Cleanup script for mql5 copy 2.md
Removes artifacts from lines 1238+ while preserving valid syntax items.
"""
import re

def should_skip_line(line):
    """Return True if the line should be removed."""
    stripped = line.strip()
    
    # Skip empty lines
    if not stripped:
        return True
    
    # Skip lines with dots (page number references like "........ 3702")
    if '..' in stripped:
        return True
    
    # Skip copyright notices
    if '© 2000-2025' in stripped or 'MetaQuotes' in stripped:
        return True
    
    # Skip page break characters with numbers (like \f25)
    if stripped.startswith('\f') or re.match(r'^\x0c\d+$', stripped):
        return True
    
    # Skip "Content" header
    if stripped == 'Content':
        return True
    
    # Skip standalone numbers (page numbers)
    if re.match(r'^\d+$', stripped):
        return True
    
    return False

def process_file(input_path, output_path, preserve_until_line=1237):
    """Process the file, preserving lines up to preserve_until_line and cleaning the rest."""
    
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    output_lines = []
    
    # Preserve the first section exactly as-is
    for i in range(min(preserve_until_line, len(lines))):
        output_lines.append(lines[i])
    
    # Process the remaining lines
    for i in range(preserve_until_line, len(lines)):
        line = lines[i]
        
        if not should_skip_line(line):
            # Clean up the line - remove CR if present, keep the content
            cleaned = line.rstrip('\r\n')
            if cleaned.strip():  # Only add non-empty lines
                output_lines.append(cleaned + '\n')
    
    # Write output
    with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(output_lines)
    
    print(f"Processed {len(lines)} input lines")
    print(f"Output {len(output_lines)} lines to {output_path}")
    print(f"Preserved first {preserve_until_line} lines, cleaned {len(lines) - preserve_until_line} lines")

if __name__ == '__main__':
    input_file = r'C:\Users\User\Desktop\VSCode\MQL5-Theme\mql5 copy 2.md'
    output_file = r'C:\Users\User\Desktop\VSCode\MQL5-Theme\mql5_cleaned.md'
    process_file(input_file, output_file)
