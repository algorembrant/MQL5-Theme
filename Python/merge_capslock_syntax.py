"""
Script to merge CAPSLOCK_NAMES_SYNTAX identifiers from mql5_capslock_syntax.md 
into syntax.md, adding them to corresponding categories.
"""

import re
from pathlib import Path
from collections import defaultdict

def parse_capslock_file(filepath: str) -> dict:
    """
    Parse mql5_capslock_syntax.md and extract all identifiers grouped by prefix.
    Returns dict: {prefix: set of identifiers}
    """
    identifiers = defaultdict(set)
    current_prefix = None
    in_code_block = False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Detect category header like "## ACCOUNT_* <a name="account"></a>"
            if line.startswith('## ') and '_*' in line:
                match = re.match(r'## ([A-Z0-9]+)_\*', line)
                if match:
                    current_prefix = match.group(1)
                    continue
            
            # Track code blocks
            if line == '```':
                in_code_block = not in_code_block
                continue
            
            # Extract identifiers inside code blocks
            if in_code_block and current_prefix and line:
                # This is an identifier
                identifiers[current_prefix].add(line)
    
    return dict(identifiers)


def parse_syntax_file(filepath: str) -> tuple:
    """
    Parse syntax.md and extract:
    1. The file structure with sections
    2. Existing identifiers in each section
    
    Returns: (lines, sections_info)
    sections_info = {section_name: {'start': line_num, 'end': line_num, 'identifiers': set}}
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    sections = {}
    current_section = None
    code_block_start = None
    code_block_end = None
    in_code_block = False
    current_identifiers = set()
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Detect section headers
        if stripped.startswith('## '):
            # Save previous section's code block if any
            if current_section and code_block_start is not None:
                sections[current_section] = {
                    'code_start': code_block_start,
                    'code_end': code_block_end,
                    'identifiers': current_identifiers
                }
            
            current_section = stripped[3:].strip()
            code_block_start = None
            code_block_end = None
            in_code_block = False
            current_identifiers = set()
            continue
        
        # Track code blocks
        if stripped == '```':
            if not in_code_block:
                in_code_block = True
                code_block_start = i
            else:
                in_code_block = False
                code_block_end = i
            continue
        
        # Extract identifiers inside code blocks
        if in_code_block and stripped:
            # Split by whitespace to get individual identifiers per line
            for ident in stripped.split():
                current_identifiers.add(ident)
    
    # Save last section
    if current_section and code_block_start is not None:
        sections[current_section] = {
            'code_start': code_block_start,
            'code_end': code_block_end,
            'identifiers': current_identifiers
        }
    
    return lines, sections


def map_prefix_to_section(prefix: str, sections: dict) -> str:
    """
    Map a CAPSLOCK prefix to the most appropriate section in syntax.md.
    Returns section name or None if no good match.
    """
    # Direct mapping based on common prefixes
    prefix_to_section = {
        'ACCOUNT': 'Account ENUM Constants (ENUM_ACCOUNT_INFO_...)',
        'CHART': 'Chart Constants (ENUM_CHART_...)',
        'CHARTEVENT': 'Chart Constants (ENUM_CHART_...)',
        'DEAL': 'Deal Constants (ENUM_DEAL_...)',
        'ORDER': 'Order Type Constants (ENUM_ORDER_TYPE)',
        'POSITION': 'Position Properties (ENUM_POSITION_PROPERTY_INTEGER/DOUBLE/STRING)',
        'SYMBOL': 'Symbol ENUM Constants (ENUM_SYMBOL_INFO_...)',
        'TRADE': 'Trade Request Actions (ENUM_TRADE_REQUEST_ACTIONS)',
        'PERIOD': 'Timeframe Constants (ENUM_TIMEFRAMES)',
        'TERMINAL': 'Terminal/Environment Constants',
        'OBJPROP': 'Object Property Constants (OBJPROP_...)',
        'OBJ': 'Object Types (ENUM_OBJECT)',
        'INIT': 'Return Codes (ENUM_INIT_RETCODE)',
        'DRAW': 'Numeric Limits',  # Drawing styles
        'FILE': 'File Functions',
        'ERR': 'Numeric Limits',
        'MODE': 'Numeric Limits',
        'INDICATOR': 'Indicator Functions',
        'IND': 'Indicator Functions',
        'PRICE': 'Numeric Limits',
        'SIGNAL': 'Signal Functions',
        'ENUM': 'Uncategorized',
        'CL': 'Standard Library Classes',
        'MQL': 'Magic/Predefined Variables',
        'CALENDAR': 'Uncategorized',
        'DATABASE': 'Uncategorized',
        'ONNX': 'Event Handler Functions',
        'CRYPT': 'Uncategorized',
        'COPY': 'Uncategorized',
        'REASON': 'Return Codes (ENUM_INIT_RETCODE)',
        'BOOK': 'Uncategorized',
        'CORNER': 'Uncategorized',
        'ANCHOR': 'Uncategorized',
        'ALIGN': 'Uncategorized',
        'BORDER': 'Uncategorized',
        'STYLE': 'Uncategorized',
        'TICK': 'Uncategorized',
        'TIME': 'Date and Time',
        'TIMEFRAME': 'Timeframe Constants (ENUM_TIMEFRAMES)',
        'STAT': 'Uncategorized',
        'DX': 'Uncategorized',
        'DXGI': 'Uncategorized',
        'OPENCL': 'Standard Library Classes',
        'LOSS': 'Uncategorized',
        'REGRESSION': 'Uncategorized',
        'MATRIX': 'Uncategorized',
        'VECTOR': 'Uncategorized',
        'PLOT': 'Indicator Functions',
        'SECTOR': 'Uncategorized',
        'INDUSTRY': 'Uncategorized',
        'THEME': 'Uncategorized',
        'SESSION': 'Uncategorized',
        'SERIES': 'Timeseries Functions',
        'COLOR': 'Color Constants',
        'POINTER': 'Uncategorized',
        'LICENSE': 'Uncategorized',
        'FW': 'Uncategorized',
        'MB': 'Uncategorized',
        'CP': 'Uncategorized',
        'CUSTOM': 'Uncategorized',
        'DBL': 'Numeric Limits',
        'FLT': 'Numeric Limits',
        'INT': 'Numeric Limits',
        'LONG': 'Numeric Limits',
        'ULONG': 'Numeric Limits',
        'SHORT': 'Numeric Limits',
        'CHAR': 'Numeric Limits',
        'FLAG': 'Uncategorized',
        'SEEK': 'File Functions',
        'KEY': 'Uncategorized',
        'MOUSE': 'Uncategorized',
        'FONT': 'Uncategorized',
        'PROGRAM': 'Uncategorized',
        'TYPE': 'Uncategorized',
        'GANN': 'Uncategorized',
        'ELLIOTT': 'Uncategorized',
        'AVERAGE': 'Uncategorized',
        'CLASSIFICATION': 'Uncategorized',
        'ARRAYPRINT': 'Array Functions',
    }
    
    return prefix_to_section.get(prefix, 'Uncategorized')


def generate_merged_file(original_lines: list, sections: dict, capslock_identifiers: dict, output_path: str):
    """
    Generate the merged syntax.md file.
    """
    # First, collect all new identifiers to add to each section
    section_additions = defaultdict(set)
    unmatched_prefixes = []
    
    for prefix, identifiers in capslock_identifiers.items():
        section_name = map_prefix_to_section(prefix, sections)
        if section_name and section_name in sections:
            # Only add identifiers that don't already exist
            existing = sections[section_name]['identifiers']
            new_idents = identifiers - existing
            section_additions[section_name].update(new_idents)
        else:
            # Add to Uncategorized
            if 'Uncategorized' in sections:
                existing = sections['Uncategorized']['identifiers']
                new_idents = identifiers - existing
                section_additions['Uncategorized'].update(new_idents)
    
    # Now rebuild the file with merged content
    output_lines = []
    skip_until_code_end = False
    current_section = None
    
    i = 0
    while i < len(original_lines):
        line = original_lines[i]
        stripped = line.strip()
        
        # Detect section headers
        if stripped.startswith('## '):
            current_section = stripped[3:].strip()
            output_lines.append(line)
            i += 1
            continue
        
        # Check if this is a code block that we need to modify
        if current_section in sections and stripped == '```':
            section_info = sections[current_section]
            
            if i == section_info['code_start']:
                # Start of code block - write merged content
                output_lines.append(line)  # Opening ```
                
                # Collect all identifiers (existing + new)
                all_identifiers = section_info['identifiers'].copy()
                if current_section in section_additions:
                    all_identifiers.update(section_additions[current_section])
                
                # Sort and format identifiers
                sorted_idents = sorted(all_identifiers)
                
                # Write identifiers in a nice format (multiple per line, similar to original)
                line_width = 0
                current_line = []
                for ident in sorted_idents:
                    if line_width + len(ident) + 2 > 80 and current_line:
                        output_lines.append('  '.join(current_line) + '\n')
                        current_line = [ident]
                        line_width = len(ident)
                    else:
                        current_line.append(ident)
                        line_width += len(ident) + 2
                
                if current_line:
                    output_lines.append('  '.join(current_line) + '\n')
                
                # Skip original code block content until closing ```
                i += 1
                while i < len(original_lines) and original_lines[i].strip() != '```':
                    i += 1
                
                output_lines.append('```\n')  # Closing ```
                i += 1
                continue
        
        output_lines.append(line)
        i += 1
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    return section_additions


def main():
    script_dir = Path(__file__).parent
    capslock_file = script_dir / "mql5_capslock_syntax.md"
    syntax_file = script_dir / "syntax.md"
    output_file = script_dir / "syntax.md"  # Overwrite original
    
    print(f"Parsing {capslock_file}...")
    capslock_identifiers = parse_capslock_file(capslock_file)
    total_capslock = sum(len(v) for v in capslock_identifiers.values())
    print(f"Found {total_capslock} CAPSLOCK identifiers in {len(capslock_identifiers)} prefixes")
    
    print(f"\nParsing {syntax_file}...")
    original_lines, sections = parse_syntax_file(syntax_file)
    print(f"Found {len(sections)} sections in syntax.md")
    
    print(f"\nMerging and writing to {output_file}...")
    additions = generate_merged_file(original_lines, sections, capslock_identifiers, output_file)
    
    total_added = sum(len(v) for v in additions.values())
    print(f"\nAdded {total_added} new identifiers across {len([k for k, v in additions.items() if v])} sections")
    
    # Print summary by section
    for section, idents in sorted(additions.items()):
        if idents:
            print(f"  - {section}: +{len(idents)} identifiers")


if __name__ == "__main__":
    main()
