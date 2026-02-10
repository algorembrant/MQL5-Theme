import re
import json
import os

markdown_file_path = r"C:\Users\User\Desktop\VSCode\MQL5-Theme\syntax_List\grouping_syntaxes_cleaned.md"
json_file_path = r"C:\Users\User\Desktop\VSCode\MQL5-Theme\syntaxes\mql5.tmLanguage.json"

# 1. Read prefixes
print(f"Reading {markdown_file_path}...")
with open(markdown_file_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

md_prefix_pattern = re.compile(r"that has '([^']+)' prefix")
md_prefixes = sorted(list(set(md_prefix_pattern.findall(md_content))))
print(f"Found {len(md_prefixes)} prefixes in markdown.")

# 2. Read existing JSON (to preserve core patterns)
print(f"Reading {json_file_path}...")
with open(json_file_path, 'r', encoding='utf-8') as f:
    tm_language = json.load(f)

# 3. Identify patterns to KEEP
# We will effectively replace the "patterns" array, but we want to seed it with
# the non-function-grouping patterns from the original file if possible, or
# just standard MQL5 patterns (comments, strings, numbers, keywords).
# However, the user said "overwrite".
# To be safe and functional, we should keep:
# - comments
# - strings
# - numeric constants
# - control keywords
# - storage types
# - preprocessor
# - standard operators?

keep_patterns = []
patterns = tm_language.get("patterns", [])

# Names of patterns we likely want to remove/replace because we are generating them
remove_pattern_names = [
    "support.function.prefix.mql5",
    "support.function.special-prefix.mql5",
    "support.function.python-style.mql5",
    "support.function.misc.mql5",
    "support.function.account-info.mql5",
    "support.function.array.mql5",
    "support.function.ctrade.mql5",
    "support.constant.chart.mql5", # Check if these are in MD? MD has 'Chart' prefix, so yes.
    "support.function.chart.mql5",
    "support.function.check.mql5",
    "support.constant.color.mql5",
    "support.function.common.mql5",
    "support.function.conversion.mql5",
    "support.function.custom-indicator.mql5",
    "support.function.datetime.mql5",
    "support.constant.deal.mql5",
    "support.function.event.mql5",
    "support.function.file.mql5",
    "support.function.global-variable.mql5",
    "support.function.indicator.mql5",
    "support.type.struct.mql5", # Struct names might be covered?
    "support.variable.predefined.mql5", # _Symbol etc covered by _ prefix?
    "support.function.market-info.mql5",
    "support.function.math.mql5",
    "support.constant.numeric-limits.mql5",
    "support.function.object.mql5",
    "support.constant.objprop.mql5",
    "support.constant.object-type.mql5",
    "support.constant.order-filling.mql5",
    "support.constant.order-state.mql5",
    "support.constant.order-time.mql5",
    "support.constant.order-type.mql5",
    "support.constant.position-type.mql5",
    "support.constant.position-property.mql5",
    "support.constant.init-retcode.mql5",
    "support.function.signal.mql5",
    "support.class.stdlib.mql5",
    "support.function.string.mql5",
    "support.constant.symbol-info.mql5",
    "support.constant.symbol-filling.mql5",
    "support.constant.symbol-trade-mode.mql5",
    "support.function.symbol-info.mql5",
    "support.constant.terminal.mql5",
    "support.function.text.mql5",
    "support.constant.timeframe.mql5",
    "support.function.timeseries.mql5",
    "support.function.trade.mql5",
    "support.constant.trade-action.mql5",
    "support.function.uncategorized.mql5"
]

# We should verify if the MD covers constants. 
# MD has: "highlights syntax ... that has 'CHART' prefix".
# JSON has `support.constant.chart.mql5`.
# If we replace `support.constant.chart.mql5` with a generic `Chart*` matcher, we lose the specific "constant" scope.
# BUT the user said: "each group ... to have different colors".
# This implies they want the "Chart" group to be colored one way.
# If I keep the specific constant group, it might overlap.
# Usually, specific matches win over generic regexes if placed earlier.
# Or if placed later? TextMate matching order depends on definition.
# I will APPEND the new generic patterns at the END.
# But logic suggests the USER wants to CONTROL these groupings via the MD.
# So I should probably disable the old detailed lists if the MD covers them generically.
# However, `support.constant.chart.mql5` matches things starting with `CHART_` or `CHARTEVENT_`.
# The MD has `Chart` prefix. `Chart` matches `ChartApplyTemplate` but NOT `CHART_EVENT`.
# Unless the MD has `CHART` prefix too? 
# Let's check MD for `CHART` or `ETH` etc.
# The user wants "each group in ... MD ... to have different colors".
# I will generate the MD patterns.
# I will KEEP any pattern that is NOT explicitly "support.function..." grouping unless it seems completely redundant.
# Actually, iterating through 580 prefixes ensures broad coverage.
# To be safe, I will keep:
# - comments, strings, numbers
# - keyword.control
# - storage.type
# - keyword.other.preprocessor
# - constant.language.boolean?
# And REMOVE all `support.*` sets that look like API lists, because the MD likely replaces them with prefix rules.

for p in patterns:
    name = p.get("name", "")
    # Keep core syntax
    if name.startswith("comment.") or \
       name.startswith("string.") or \
       name.startswith("constant.numeric.") or \
       name.startswith("constant.language.") or \
       name.startswith("keyword.control") or \
       name.startswith("keyword.other.preprocessor") or \
       name.startswith("storage.type") or \
       name == "variable.other.input.mql5" or \
       name == "constant.other.caps.mql5": 
       # matched CAPS are constant?
       keep_patterns.append(p)

    # We skip all support.* patterns as they are likely the ones being replaced by dynamic prefixes

# 4. Generate new patterns from prefixes
new_patterns = []
generated_count = 0

for prefix in md_prefixes:
    if not prefix: continue
    
    # regex logic:
    # If prefix is "Chart", we want to match "ChartMatches..."
    # Pattern: \bPrefix\w*\b
    # Prefix "Chart" -> \bChart\w*\b
    # Prefix "_" -> \b_\w*\b (matches _Symbol, _Digits)
    
    # Sanitize prefix for regex? (escape special chars if any, but they seem to be identifiers)
    escaped_prefix = re.escape(prefix)
    
    # Ensure it starts at word boundary?
    # Yes, usually functions start at boundary.
    # Pattern:
    regex = f"\\b{escaped_prefix}\\w*\\b"
    
    # Check if prefix starts with symbol?
    if not prefix[0].isalnum() and prefix[0] != '_':
        # e.g. . or # (hash is preprocessor)
        # If prefix is `#`, \b# matches nothing.
        # But MD prefixes look like identifier prefixes.
        pass

    # Scope name:
    # support.function.prefix.PREFIX_LOWER.mql5
    # or just support.function.PREFIX.mql5
    # To facilitate "different colors", having a unique component is key.
    # Using lowercase for standard convention, but uppercase is fine in scope names.
    # Let's use valid scope chars: [a-z0-9.-]
    safe_name = re.sub(r'[^a-zA-Z0-9]', '-', prefix).lower()
    scope = f"support.function.prefix.{safe_name}.mql5"
    
    pattern_obj = {
        "match": regex,
        "name": scope
    }
    
    new_patterns.append(pattern_obj)
    generated_count += 1

# 5. Assemble and Write
# Put existing core patterns FIRST, then the new specific patterns.
# Note: existing "constant.other.caps.mql5" matches ALL CAPS.
# If I put it before, `CHART_EVENT` matches CAPS.
# If I put "Chart" prefix pattern after, does it match? "Chart" doesn't match "CHART".
# MD might contain "CHART" prefix?
# If MD contains "CHART", and I generate `\bCHART\w*\b`, it overlaps with `constant.other.caps`.
# Standard TextMate rule: first match wins.
# If I want the user's Prefix groups to take precedence (to have their specific colors), I should put them BEFORE the generic fallbacks.
# So:
# 1. Comments/Strings (highest priority structure)
# 2. Generated Prefix Patterns (specificAPI groups)
# 3. Generic Fallbacks (Keyword control, caps constants, numbers)

# Wait, `keyword.control` (if, while) should definitely be highlighted as keywords, not as a prefix group (unless "if" is in prefix list?).
# "if" is likely NOT in prefix list.
# But some prefixes might overlap with keywords? e.g. "Color" vs "color" type?
# "color" is type. Prefix "Color" (capital C) is different.
# If MD has "color" (lowercase), then it might shadow `storage.type`.
# I'll put Generated Patterns AFTER Comments/Strings, but BEFORE generic identifiers/caps.
# But `keyword.control` and `storage.type` are typically specific and should be high priority.

# Let's split keep_patterns into "High Priority" and "Low Priority".
high_prio = []
low_prio = []

for p in keep_patterns:
    name = p.get("name", "")
    if name.startswith("comment") or name.startswith("string"):
        high_prio.append(p)
    else:
        low_prio.append(p) # keywords, types, numbers, caps

# Actually, keywords/types are very specific. `int` matches exactly `\bint\b`.
# Prefix `in` matches `\bin\w*\b`. e.g. `initialize`.
# Does `\bin\w*\b` match `int`? Yes.
# If `in` is a prefix in MD, and I put it before shortcuts, `in...` scope will shadow `int` type scope.
# The user wants "different colors" for the *prefixed* groups.
# It is safer to place specific keywords/types *before* the generic prefix matchers.
# Ensure `int` is matched as type.
# Then `initialize` (not matched by int) is matched by `in` prefix.

final_patterns = high_prio + low_prio + new_patterns

tm_language["patterns"] = final_patterns

print(f"Rebuilt patterns. Total: {len(final_patterns)} (Generated: {generated_count})")
print(f"Writing to {json_file_path}...")
with open(json_file_path, 'w', encoding='utf-8') as f:
    json.dump(tm_language, f, indent=4)

print("Done.")
