import re

def clean_syntax(line):
    # Remove page break character
    line = line.replace('\x0c', '')
    
    # Remove dots and following numbers (page numbers in TOC)
    line = re.sub(r'\.\.\.+.*', '', line)
    
    # Strip whitespace
    line = line.strip()
    
    # If line is empty or just numbers, skip
    if not line or line.isdigit():
        return None
        
    # Remove "doubles" separated by space (like "MathAbs MathAbs" or common typos like "Arcc os")
    # Actually, the user says "delete anything that it double (separated with space)"
    # Examples from file: "Char, Short, Int and Long Types", "MathArc c os"
    
    # If there's a space, check if it's a double or a split word
    if ' ' in line:
        parts = line.split()
        if len(parts) == 2 and parts[0] == parts[1]:
            line = parts[0]
        elif len(parts) > 1:
            # Check for things like "MathArc c os" -> "MathArccos"
            # This is tricky because "Data Types" is valid.
            # But the user says "SingleSyntax".
            # If we assume syntaxes don't have spaces, we can join them or take the first part.
            # However, MQL5 syntaxes like OBJ_VLINE don't have spaces.
            # Let's try to join parts if they look like they were split by mistake (single chars etc)
            # or just take the first part if it looks like a keyword.
            
            # If it's something like "Char, Short, Int and Long Types", it's a header.
            # If it's something like "MathArc c os", we want "MathArccos".
            # Let's join them and see if it looks like a syntax.
            joined = "".join(parts)
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', joined):
                line = joined
            else:
                # If it's a list or header, maybe skip it or just take individual words?
                # The user wants "SingleSyntax". 
                # Let's filter for things that look like identifiers.
                return None 

    # Final check: Must look like an MQL5 identifier (starts with letter or _, contains alphanumeric/_)
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', line):
        # Exclude common noise
        noise = {'Content', 'MQL5', 'Reference', 'MetaQuotes', 'Ltd', 'Language', 'Basics', 'Page', 'Content'}
        if line in noise:
            return None
        return line
    
    return None

def main():
    input_file = r'c:\Users\User\Desktop\VSCode\MQL5-Theme\mql5 copy.md'
    output_file = r'c:\Users\User\Desktop\VSCode\MQL5-Theme\mql5_syntax_extracted.md'
    
    unique_syntaxes = set()
    ordered_syntaxes = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                syntax = clean_syntax(line)
                if syntax and syntax not in unique_syntaxes:
                    unique_syntaxes.add(syntax)
                    ordered_syntaxes.append(syntax)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in ordered_syntaxes:
                f.write(f"{item}\n")
        
        print(f"Extraction complete. {len(ordered_syntaxes)} unique syntaxes saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
