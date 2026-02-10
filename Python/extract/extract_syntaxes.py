
import re
import os

def extract_syntaxes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    syntaxes = []
    
    # improved regex to capture function definitions across multiple lines
    # Pattern: ReturnType FunctionName( ... );
    # We look for a line starting with a type, then a function name, then '(', then anything until ');'
    # We exclude lines that look like text or other things.
    
    # Regex breakdown:
    # ^\s*                                      # Start of line, optional whitespace
    # (?:const\s+)?                             # Optional 'const'
    # (?:\w+(?:<[^>]+>)?::)?                    # Optional Class:: or Class<T>::
    # \w+(?:<[^>]+>)?                           # Return Type (word potentially with templates)
    # (?:&|\*)?                                 # Optional reference or pointer char
    # \s+                                       # Whitespace
    # (\w+(?:::\w+)?)                           # Function Name (Group 1), potentially Class::Method
    # \s*                                       # Optional whitespace
    # \(                                        # Opening parenthesis
    # (?:[^;]*)                                 # Content arguments (non-greedy, but allowing newlines)
    # \);                                       # Closing parenthesis and semicolon
    
    # This is tricky because of the multi-line nature and potential false positives.
    # Let's try a block-based approach. 
    # We look for the pattern Start -> End.
    
    # Common signature pattern in this file seems to be:
    # Type FunctionName(
    #    params
    #    );
    
    # Let's simple regex for potential function starts, then validate.
    
    func_start_pattern = re.compile(r'^\s*(?:const\s+)?(\w+(?:<[^>]+>)?(?:&|\*)?)\s+(\w+(?:::\w+)?)\s*\($')
    
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        match = func_start_pattern.match(lines[i]) # Using original line to check indentation if needed, but signature usually starts at beginning or indented?
        # Alert example: "void Alert(" is at start of line? No, indentation in text might vary.
        # Let's assume standard formatting from the dump.
        
        if match:
            # Found potential start
            # Check if it ends with ); in subsequent lines
            current_syntax = [lines[i]]
            j = i + 1
            complete = False
            while j < len(lines) and j < i + 20: # Limit lookahead
                current_syntax.append(lines[j])
                if ');' in lines[j]:
                    complete = True
                    break
                j += 1
            
            if complete:
                full_syntax = '\n'.join(current_syntax)
                # Filter out garbage
                if "©" not in full_syntax and "..." not in full_syntax and "Example:" not in full_syntax:
                     syntaxes.append(full_syntax)
                i = j 
        
        # Enums
        # enum Name
        # {
        # ...
        # };
        elif line.startswith('enum ') and '{' not in line: 
             # Check next line for {
             if i+1 < len(lines) and lines[i+1].strip() == '{':
                current_syntax = [lines[i]]
                j = i + 1
                while j < len(lines) and j < i + 50:
                    current_syntax.append(lines[j])
                    if '};' in lines[j]:
                        syntaxes.append('\n'.join(current_syntax))
                        i = j
                        break
                    j += 1
        
        # Structs
        elif line.startswith('struct ') and '{' not in line:
             if i+1 < len(lines) and lines[i+1].strip() == '{':
                current_syntax = [lines[i]]
                j = i + 1
                while j < len(lines) and j < i + 50:
                    current_syntax.append(lines[j])
                    if '};' in lines[j]:
                        syntaxes.append('\n'.join(current_syntax))
                        i = j
                        break
                    j += 1

        i += 1

    return syntaxes

def main():
    mql5_path = r'C:\Users\User\Desktop\VSCode\MQL5-Theme\Python\mql5.md'
    output_path = r'C:\Users\User\Desktop\VSCode\MQL5-Theme\mores.md'
    
    if not os.path.exists(mql5_path):
        print(f"File not found: {mql5_path}")
        return

    print("Extracting syntaxes...")
    extracted = extract_syntaxes(mql5_path)
    print(f"Found {len(extracted)} syntax blocks.")
    
    with open(output_path, 'a', encoding='utf-8') as f: # Append mode
        f.write('\n\n## Extracted Syntaxes\n\n')
        for block in extracted:
            f.write('```mql5\n')
            f.write(block)
            f.write('\n```\n\n')

if __name__ == '__main__':
    main()
