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
        
    # User requirement: "only skip those who had separated by 'spacing' because all type of syntaxes is okay"
    if ' ' in line:
        parts = line.split()
        if len(parts) >= 1 and all(p == parts[0] for p in parts):
            # All parts are the same word repeated, take one
            line = parts[0]
        else:
            # Multiple different words on one line -> Discard (likely a header or sentence)
            return None

    # Final noise check: ensure it contains at least one letter or digit
    # This avoids lines that are just symbols (e.g. "•", "#", etc.)
    if not re.search(r'[a-zA-Z0-9]', line):
        return None
            
    return line

def main():
    input_file = r'c:\Users\User\Desktop\VSCode\MQL5-Theme\mql5 copy.md'
    output_file = r'c:\Users\User\Desktop\VSCode\MQL5-Theme\mql5_syntax_extracted_1.md'
    
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
