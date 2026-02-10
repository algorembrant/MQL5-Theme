import re
import json
import os

markdown_file_path = r"C:\Users\User\Desktop\VSCode\MQL5-Theme\syntax_List\grouping_syntaxes_cleaned.md"
json_file_path = r"C:\Users\User\Desktop\VSCode\MQL5-Theme\syntaxes\mql5.tmLanguage.json"

# 1. Extract prefixes from markdown
print(f"Reading {markdown_file_path}...")
with open(markdown_file_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

# Regex to find prefixes in the markdown structure
# pattern look for: that has 'PREFIX' prefix
md_prefix_pattern = re.compile(r"that has '([^']+)' prefix")
md_prefixes = set(md_prefix_pattern.findall(md_content))

print(f"Found {len(md_prefixes)} prefixes in markdown file.")

# 2. Read JSON file
print(f"Reading {json_file_path}...")
with open(json_file_path, 'r', encoding='utf-8') as f:
    tm_language = json.load(f)

# 3. Find the target pattern in JSON
target_name = "support.function.prefix.mql5"
target_pattern_obj = None

if "patterns" in tm_language:
    for pattern in tm_language["patterns"]:
        if pattern.get("name") == target_name:
            target_pattern_obj = pattern
            break

if not target_pattern_obj:
    print(f"Error: Could not find pattern with name '{target_name}' in JSON.")
    exit(1)

# 4. Extract existing prefixes from JSON regex
# Expected format: "\\b(Prefix1|Prefix2|...)[A-Z0-9_]\\w*\\b"
# We need to parse the group inside \\b(...)[A-Z0-9_]
current_match = target_pattern_obj["match"]
print(f"Current match regex: {current_match}")

# Start by trying to extract the content inside the first capturing group
# This regex assumes the standard structure: \b(group)...\b
# It looks for content between `\b(` and `)` that comes before `[` or end of line/word boundary
regex_wrapper_pattern = re.compile(r"\\b\((.*?)\)(?:\[|\\b)")
match_group = regex_wrapper_pattern.search(current_match)

existing_prefixes = set()
if match_group:
    group_content = match_group.group(1)
    existing_prefixes = set(group_content.split('|'))
    print(f"Found {len(existing_prefixes)} existing prefixes in JSON.")
else:
    print("Warning: Could not parse existing prefixes from regex. Starting fresh with markdown prefixes.")

# 5. Merge prefixes
# We want to add all md_prefixes.
# We also want to keep existing ones if they are not invalid.
# The user wants to "follow what is written on ... grouping_syntaxes_cleaned.md"
# This implies the markdown is the source of truth for the *additions* or *consolidations*.
# However, we should merge carefully.
merged_prefixes = existing_prefixes.union(md_prefixes)

# Remove empty strings if any
merged_prefixes = {p for p in merged_prefixes if p}

# 6. Sort prefixes
# Sorting by length descending is crucial for regex alternation to match longest first (e.g. 'Co' vs 'Copy')
# Then alphabetical for determinism
sorted_prefixes = sorted(list(merged_prefixes), key=lambda x: (-len(x), x))

# 7. Construct new regex
# Reconstruct the regex. We need to preserve the suffix part: `[A-Z0-9_]\\w*\\b` from the original if possible,
# or use a standard one.
# The original was: "\\b(File|...)[A-Z0-9_]\\w*\\b"
# The suffix `[A-Z0-9_]\\w*\\b` ensures we match things that start with the prefix followed by valid identifier chars,
# effectively acting as a prefix matcher for function calls/types.

# Check if original had a suffix
suffix = "[A-Z0-9_]\\w*\\b" # Default fallback
if match_group:
    # Try to find what came after the group
    span = match_group.span(1)
    # end of group content is span[1]
    # closing paren is span[1] + (index in string)
    # The regex structure in python string is literal backslashes.
    # match_group.end(0) gives the end of the `\b(...)` part roughly if we matched `\b(` and `)`
    # Let's just be safer and assume the standard suffix if we can't easily parse it, 
    # OR reuse the suffix from the original string if we can locate the splits.
    
    # Simple approach: The original string is `\b(A|B|C)[suffix]`
    # We replace `A|B|C` with joined new prefixes.
    
    # Locate the start and end of the list in the original string
    start_index = match_group.start(1)
    end_index = match_group.end(1)
    
    prefix_part = current_match[:start_index]
    suffix_part = current_match[end_index:]
    
    new_match_content = "|".join(sorted_prefixes)
    new_regex = prefix_part + new_match_content + suffix_part
else:
    # Fallback construction
    new_match_content = "|".join(sorted_prefixes)
    new_regex = f"\\b({new_match_content})[A-Z0-9_]\\w*\\b"

print(f"New match regex length: {len(new_regex)}")
# print(f"New match sample: {new_regex[:100]}...")

# 8. Update JSON object
target_pattern_obj["match"] = new_regex

# 9. Write JSON file
print(f"Writing updates to {json_file_path}...")
with open(json_file_path, 'w', encoding='utf-8') as f:
    json.dump(tm_language, f, indent=4)

print("Done.")
