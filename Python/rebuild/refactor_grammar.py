
import re
import json
import random
import colorsys

def generate_distinct_colors(n):
    colors = []
    for i in range(n):
        hue = i / n
        saturation = 0.7 + (random.random() * 0.3)  # 0.7-1.0
        lightness = 0.4 + (random.random() * 0.4)   # 0.4-0.8 for visibility
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        hex_color = "#{:02x}{:02x}{:02x}".format(
            int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
        )
        colors.append(hex_color)
    return colors

def main():
    example_md_path = r'c:\Users\User\Desktop\VSCode\MQL5-Theme\example.md'
    grammar_path = r'c:\Users\User\Desktop\VSCode\MQL5-Theme\syntaxes\mql5.tmLanguage.json'
    package_json_path = r'c:\Users\User\Desktop\VSCode\MQL5-Theme\package.json'

    # 1. Parse example.md for prefixes
    prefixes = []
    try:
        with open(example_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Regex to find: has 'Prefix' prefix
            matches = re.finditer(r"has '([^']+)' prefix", content)
            for match in matches:
                prefix = match.group(1)
                if prefix not in prefixes:
                    prefixes.append(prefix)
    except Exception as e:
        print(f"Error reading example.md: {e}")
        return

    print(f"Found {len(prefixes)} unique prefixes.")

    # 2. Generate Grammar Patterns
    grammar_patterns = []
    
    # Add comments
    grammar_patterns.append({
        "begin": "//",
        "end": "$",
        "name": "comment.line.double-slash.mql5"
    })
    grammar_patterns.append({
        "begin": "/\\*",
        "end": "\\*/",
        "name": "comment.block.mql5"
    })
    
    # Add strings
    grammar_patterns.append({
        "begin": "\"",
        "end": "\"",
        "name": "string.quoted.double.mql5",
        "patterns": [{"match": "\\\\.", "name": "constant.character.escape.mql5"}]
    })
    
    # Add numbers
    grammar_patterns.append({
        "match": "\\b\\d+(\\.\\d+)?\\b",
        "name": "constant.numeric.mql5"
    })

    # Add Prefix Patterns
    # Sort prefixes by length (longest first) to prevent partial matching issues if any overlap
    sorted_prefixes = sorted(prefixes, key=len, reverse=True)
    
    for prefix in sorted_prefixes:
        # Construct scope name: support.function.prefix.<Prefix>.mql5
        scope_name = f"support.function.prefix.{prefix}.mql5"
        
        # Regex: \bPrefix[A-Z0-9_]\w*\b
        # This matches the Prefix followed immediately by an uppercase letter, digit, or underscore, then remaining word chars.
        # This assumes standard MQL5 naming conventions like PrefixSomething or PREFIX_SOMETHING
        # If the prefix is 'Alert', it matches 'AlertMe', 'Alert_Error'. 
        # It ensures we don't just match 'Alert' alone if it requires a suffix, 
        # BUT the requirement says "identifies prefixes then automatically colors the rest part of the syntax".
        # If 'Alert' itself is a valid function, we should matched strictly or with suffix.
        # Given the prompt "identifies prefixes then automatically colors the rest part of the syntax", 
        # let's assume valid MQL5 identifiers starting with the prefix.
        
        pattern = {
            "match": f"\\b{re.escape(prefix)}[A-Za-z0-9_]*\\b",
            "name": scope_name
        }
        grammar_patterns.append(pattern)

    # Fallback/General Pattern for other things? 
    # The user said "never specify a full syntax", so we mainly rely on these prefixes.
    
    new_grammar = {
        "$schema": "https://raw.githubusercontent.com/martinring/tmlanguage/master/tmlanguage.json",
        "name": "MQL5",
        "patterns": grammar_patterns,
        "scopeName": "source.mql5"
    }

    # 3. Generate Package.json Colors
    try:
        with open(package_json_path, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
    except Exception as e:
        print(f"Error reading package.json: {e}")
        return

    # Generate distinct colors
    colors = generate_distinct_colors(len(prefixes))
    
    text_mate_rules = []
    
    # Add standard rules first (comments, strings, etc)
    text_mate_rules.append({
        "name": "Comments",
        "scope": ["comment.line.double-slash.mql5", "comment.block.mql5"],
        "settings": {"foreground": "#6A9955"}
    })
    text_mate_rules.append({
        "name": "Strings",
        "scope": "string.quoted.double.mql5",
        "settings": {"foreground": "#CE9178"}
    })
    text_mate_rules.append({
        "name": "Numbers",
        "scope": "constant.numeric.mql5",
        "settings": {"foreground": "#B5CEA8"}
    })

    # Add Prefix Rules
    for i, prefix in enumerate(sorted_prefixes):
        scope_name = f"support.function.prefix.{prefix}.mql5"
        text_mate_rules.append({
            "name": f"Prefix {prefix}",
            "scope": scope_name,
            "settings": {
                "foreground": colors[i]
            }
        })

    # Update package.json structure
    if 'contributes' not in package_data:
        package_data['contributes'] = {}
    
    if 'configurationDefaults' not in package_data['contributes']:
        package_data['contributes']['configurationDefaults'] = {}
        
    if '[mql5]' not in package_data['contributes']['configurationDefaults']:
         package_data['contributes']['configurationDefaults']['[mql5]'] = {}
         
    package_data['contributes']['configurationDefaults']['[mql5]']["editor.tokenColorCustomizations"] = {
        "textMateRules": text_mate_rules
    }

    # 4. Write Files
    try:
        with open(grammar_path, 'w', encoding='utf-8') as f:
            json.dump(new_grammar, f, indent=4)
        print("Updated grammar file.")
        
        with open(package_json_path, 'w', encoding='utf-8') as f:
            json.dump(package_data, f, indent=4)
        print("Updated package.json file.")
        
    except Exception as e:
        print(f"Error writing files: {e}")

if __name__ == "__main__":
    main()
