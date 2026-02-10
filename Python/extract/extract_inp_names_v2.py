
import re
import os
import sys

# Configuration
input_file = r"c:\Users\User\Desktop\VSCode\MQL5-Theme\mql5.md"
output_file = r"c:\Users\User\Desktop\VSCode\MQL5-Theme\extracted_Inp_list.md"

def extract_inp_names(input_path, output_path):
    print(f"Starting extraction...", flush=True)
    print(f"Reading from: {input_path}", flush=True)
    
    unique_names = set()
    
    try:
        if not os.path.exists(input_path):
            print(f"Error: Input file does not exist: {input_path}")
            return

        with open(input_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f):
                # Better regex:
                full_matches = re.findall(r"\b(?:Inp|INP)[a-zA-Z0-9_]+", line)
                if full_matches:
                    unique_names.update(full_matches)
                
                if line_num % 100000 == 0:
                     print(f"Processed {line_num} lines...", flush=True)
                
        sorted_names = sorted(list(unique_names))
        
        print(f"Found {len(sorted_names)} unique names.", flush=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# Extracted 'Inp' Names from {os.path.basename(input_path)}\n\n")
            f.write(f"Total found: {len(sorted_names)}\n\n")
            for name in sorted_names:
                f.write(f"- {name}\n")
                
        print(f"Successfully written to: {output_path}", flush=True)
        
    except Exception as e:
        print(f"Error: {e}", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    extract_inp_names(input_file, output_file)
