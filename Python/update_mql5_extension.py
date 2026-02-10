import json
import os
import colorsys

# Configuration
PREFIXES_FILE = 'prefixes.md'
PACKAGE_JSON_FILE = 'package.json'
GRAMMAR_FILE = 'syntaxes/mql5.tmLanguage.json'

def generate_colors(n):
    """Generates n unique colors using HSL."""
    colors = []
    for i in range(n):
        hue = i / n
        # Use high saturation and value/lightness for visibility on both dark/light
        # Slightly varying saturation/lightness to add more distinction
        saturation = 0.6 + (i % 2) * 0.2  # 0.6 or 0.8
        lightness = 0.4 + (i % 3) * 0.1   # 0.4, 0.5, 0.6
        
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        hex_color = '#{:02x}{:02x}{:02x}'.format(
            int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
        )
        colors.append(hex_color)
    return colors

def main():
    print(f"Reading {PREFIXES_FILE}...")
    with open(PREFIXES_FILE, 'r') as f:
        # Filter lines that look like prefixes (non-empty)
        prefixes = [line.strip() for line in f if line.strip()]

    print(f"Found {len(prefixes)} prefixes.")
    if len(prefixes) != 557:
        print(f"Warning: Expected 557 prefixes, found {len(prefixes)}. Proceeding anyway.")

    # Sort prefixes by length descending to fix shadowing
    sorted_prefixes = sorted(prefixes, key=len, reverse=True)
    
    unique_colors = generate_colors(len(prefixes))
    
    # 1. Update Grammar File (mql5.tmLanguage.json)
    print(f"Updating {GRAMMAR_FILE}...")
    with open(GRAMMAR_FILE, 'r') as f:
        grammar = json.load(f)

    # Base patterns (comments, strings, numbers)
    # We will rebuild 'patterns'
    new_patterns = [
        {
            "begin": "//",
            "end": "$",
            "name": "comment.line.double-slash.mql5"
        },
        {
            "begin": "/\\*",
            "end": "\\*/",
            "name": "comment.block.mql5"
        },
        {
            "begin": "\"",
            "end": "\"",
            "name": "string.quoted.double.mql5",
            "patterns": [
                {
                    "match": "\\\\.",
                    "name": "constant.character.escape.mql5"
                }
            ]
        },
        {
            "match": "\\b\\d+(\\.\\d+)?\\b",
            "name": "constant.numeric.mql5"
        }
    ]

    # Add prefix patterns
    for prefix in sorted_prefixes:
        # Scope name matches the prefix
        scope_name = f"support.function.prefix.{prefix}.mql5"
        pattern = {
            "match": f"\\b{prefix}[A-Za-z0-9_]*\\b",
            "name": scope_name
        }
        new_patterns.append(pattern)

    grammar['patterns'] = new_patterns
    
    with open(GRAMMAR_FILE, 'w') as f:
        json.dump(grammar, f, indent=4)


    # 2. Update Package.json
    print(f"Updating {PACKAGE_JSON_FILE}...")
    with open(PACKAGE_JSON_FILE, 'r') as f:
        package_json = json.load(f)

    # Clean existing customization
    text_mate_rules = [
        {
            "name": "Comments",
            "scope": [
                "comment.line.double-slash.mql5",
                "comment.block.mql5"
            ],
            "settings": {
                "foreground": "#6A9955"
            }
        },
        {
            "name": "Strings",
            "scope": "string.quoted.double.mql5",
            "settings": {
                "foreground": "#CE9178"
            }
        },
        {
            "name": "Numbers",
            "scope": "constant.numeric.mql5",
            "settings": {
                "foreground": "#B5CEA8"
            }
        }
    ]

    # Add rules for each prefix with unique color
    # NOTE: map original prefixes (unsorted list for stable color assignment if desired, or just iterate sorted)
    # We'll stick to sorted_prefixes to align with grammar, but it doesn't strictly matter for color assignment order
    # as long as scope names match.
    for i, prefix in enumerate(sorted_prefixes):
        scope_name = f"support.function.prefix.{prefix}.mql5"
        rule = {
            "name": f"Prefix {prefix}",
            "scope": scope_name,
            "settings": {
                "foreground": unique_colors[i]
            }
        }
        text_mate_rules.append(rule)

    # Ensure structure exists
    if 'contributes' not in package_json:
        package_json['contributes'] = {}
    if 'configurationDefaults' not in package_json['contributes']:
        package_json['contributes']['configurationDefaults'] = {}
    package_json['contributes']['configurationDefaults']['editor.tokenColorCustomizations'] = {
        "textMateRules": text_mate_rules
    }

    with open(PACKAGE_JSON_FILE, 'w') as f:
        json.dump(package_json, f, indent=4)

    print("Success! Files updated.")

if __name__ == "__main__":
    main()
