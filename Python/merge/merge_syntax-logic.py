import re
import json
import os

target_file = r"C:\Users\User\Desktop\VSCode\MQL5-Theme\syntaxes\mql5.tmLanguage.json"
source_file = r"C:\Users\User\Desktop\VSCode\MQL5-Theme\syntaxes\script.json"

print(f"Reading target: {target_file}")
with open(target_file, 'r', encoding='utf-8') as f:
    target_data = json.load(f)

print(f"Reading source: {source_file}")
with open(source_file, 'r', encoding='utf-8') as f:
    source_data = json.load(f)

# 1. Analyze Target Coverage
# We need to know what prefixes are active.
# Format: "match": "\\bPrefix\\w*\\b"
# We extract "Prefix"
target_prefixes = set()
target_exact_matches = set() # For keywords, types, etc.

coverage_pattern = re.compile(r"\\b([a-zA-Z0-9_]+)\\w\*\\b") # Matches prefix logic
exact_pattern_simple = re.compile(r"\\b\(([^\)]+)\)\\b") # Matches simple lists (A|B|C)

for pattern in target_data.get("patterns", []):
    match = pattern.get("match", "")
    name = pattern.get("name", "")
    
    # Check for prefix logic
    pm = coverage_pattern.search(match)
    if pm and "*" in match: # basic heuristic for prefix pattern
        prefix = pm.group(1)
        # Verify it's not actually an exact match regex disguised
        # The prefix pattern was constructed as \bPREFIX\w*\b
        # Python's re.escape might have been used, but identifiers are usually safe.
        target_prefixes.add(prefix)
    
    # Check for exact matches (keywords, etc)
    # \b(int|void|...)\b
    em = exact_pattern_simple.search(match)
    if em and "*" not in match:
        content = em.group(1)
        # Split by |
        items = content.split('|')
        for item in items:
            target_exact_matches.add(item)

print(f"Target has {len(target_prefixes)} prefix rules.")
print(f"Target has {len(target_exact_matches)} exact match keywords (approx).")

# 2. Iterate Source patterns and filter
# We want to add patterns from Source if they carry logic NOT in Target.
# Logic is "not in Target" if the items it matches are NOT covered by Target prefixes OR Target exact matches.

new_patterns = []
skipped_count = 0
added_count = 0

for pattern in source_data.get("patterns", []):
    match = pattern.get("match", "")
    name = pattern.get("name", "")
    
    # Check what this pattern matches
    # Is it a list? \b(A|B|C)\b
    em = exact_pattern_simple.search(match)
    
    if em and "*" not in match:
        content = em.group(1)
        items = content.split('|')
        
        needed_items = []
        for item in items:
            # Check if covered by prefix
            is_covered = False
            for prefix in target_prefixes:
                if item.startswith(prefix):
                    is_covered = True
                    break
            
            # Check if covered by exact match in target (e.g. keywords)
            if not is_covered:
                if item in target_exact_matches:
                    is_covered = True
            
            if not is_covered:
                needed_items.append(item)
        
        if needed_items:
            # If we have items that need adding, we create a new pattern for them.
            # We keep the original name scope.
            
            # Optimization: If needed_items is essentially the same as original items (minus a few),
            # we just create a valid regex.
            # If needed_items is empty, we skip entirely.
            
            new_regex = "\\b(" + "|".join(needed_items) + ")\\b"
            new_p = pattern.copy()
            new_p["match"] = new_regex
            new_patterns.append(new_p)
            added_count += 1
            # print(f"Adding partial pattern for {name}: {len(needed_items)} items (e.g. {needed_items[:3]})")
        else:
            skipped_count += 1
            # print(f"Skipping fully covered pattern: {name}")

    else:
        # It's a complex regex or a single item regex or a prefix regex
        # e.g. \b\d+(\.\d+)?\b
        # or \bInp\w+\b
        
        # Heuristic:
        # If it looks like a prefix regex \bInp\w+\b
        # We check if 'Inp' is in target_prefixes.
        pm = coverage_pattern.search(match)
        if pm and "*" in match:
            prefix = pm.group(1)
            if prefix in target_prefixes:
                skipped_count += 1
                continue
            
            # Check if any target prefix covers this prefix?
            # e.g. Target has 'In', Source has 'Inp'. 'In' covers 'Inp'.
            covered = False
            for tp in target_prefixes:
                if prefix.startswith(tp):
                    covered = True
                    break
            if covered:
                skipped_count += 1
                continue

        # If it is \bval\b (single exact match not in group)
        # Check coverage
        simple_match = re.match(r"^\\b(\w+)\\b$", match)
        if simple_match:
            word = simple_match.group(1)
            is_covered = False
            for prefix in target_prefixes:
                if word.startswith(prefix):
                    is_covered = True
                    break
            if word in target_exact_matches:
                is_covered = True
            
            if is_covered:
                skipped_count += 1
                continue

        # If we are here, it's a pattern we probably want (comments, strings, numbers, or complex regexes not covered)
        # But wait, Target ALREADY HAS core syntax (comments, strings, numbers) from the rebuild step.
        # I should check if Target has a pattern with the SAME name or SAME regex?
        # Rebuild step preserved "comment...", "string...", "constant.numeric...".
        # Source has them too.
        # We should avoid adding duplicates of core syntax.
        
        # Check if identical pattern exists in target
        is_duplicate = False
        for tp in target_data.get("patterns", []):
            if tp.get("match") == match and tp.get("name") == name:
                is_duplicate = True
                break
            if tp.get("begin") == pattern.get("begin") and tp.get("end") == pattern.get("end"):
                # block pattern check (comments/strings)
                is_duplicate = True
                break
        
        if is_duplicate:
            skipped_count += 1
            continue

        # If not duplicate and not covered, Add it
        new_patterns.append(pattern)
        added_count += 1
        # print(f"Adding special pattern: {name} / {match[:30]}...")

print(f"Skipped {skipped_count} redundant patterns.")
print(f"Adding {added_count} new patterns.")

# 3. Write
# Append new patterns to the end of Target patterns
# to ensure they don't override the specific prefix matches (unless they are specific exact matches?)
# Specific exact matches (keywords) should arguably be FIRST?
# But if I put them last, and prefix matches first:
# TextMate: First Match Wins.
# Prefix: \bOrder\w*\b matches OrderSend.
# Source: \bOrderSend\b matches OrderSend.
# If Prefix is first, it wins. Scope is `support.function.prefix.order...`.
# If Source is first, it wins. Scope is `support.function.trade...`.
# User said "wanted each group in cleaned.md to have different colors".
# This implies PREFIX coloring is preferred for items covered by prefixes.
# So Prefix Rules should come FIRST.
# New patterns (which are by definition NOT covered by prefixes) can come after.
# EXCEPT for keywords/types that I might have missed in the prefix list?
# If I missed `void` in prefix list (likely), and I add it now.
# If I put it last, it works (unless caught by something else).
# So appending is safe for "not covered" items.

target_data["patterns"].extend(new_patterns)

print(f"Writing updated target to {target_file}...")
with open(target_file, 'w', encoding='utf-8') as f:
    json.dump(target_data, f, indent=4)

print("Merge Complete.")
