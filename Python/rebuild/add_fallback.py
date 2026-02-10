import json
import os
import string

target_file = r"C:\Users\User\Desktop\VSCode\MQL5-Theme\syntaxes\mql5.tmLanguage.json"

print(f"Reading target: {target_file}")
with open(target_file, 'r', encoding='utf-8') as f:
    target_data = json.load(f)

# Define fallback patterns for A-Z
# The user wants "color a or A to z or Z with different colors individually"
# Scope format: support.function.fallback.a.mql5, support.function.fallback.b.mql5, etc.

fallback_patterns = []

for char in string.ascii_lowercase:
    # Pattern: \b[aA]\w*\b
    # Note: \b ensures start of word (or end of previous non-word char)
    # [aA] matches the letter regardless of case
    # \w* matches rest of identifier
    # \b ensures end of word
    
    # Wait, the user said "single syntax that may have non-space or '_' connector"
    # identifiers in MQL5 can have underscores.
    # \w matches [a-zA-Z0-9_] in Python regex (and usually TextMate regex).
    # So \w* covers identifiers.
    
    char_upper = char.upper()
    regex = f"\\b[{char}{char_upper}]\\w*\\b"
    scope = f"support.function.fallback.{char}.mql5"
    
    pattern = {
        "match": regex,
        "name": scope
    }
    fallback_patterns.append(pattern)

print(f"Generated {len(fallback_patterns)} fallback patterns.")

# Append to END of patterns list
target_data["patterns"].extend(fallback_patterns)

print(f"Writing updated target to {target_file}...")
with open(target_file, 'w', encoding='utf-8') as f:
    json.dump(target_data, f, indent=4)

print("Add Fallback Complete.")
