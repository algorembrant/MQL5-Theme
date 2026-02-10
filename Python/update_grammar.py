
import json
import re
import sys

print("Starting script...")

# Read prefixes
prefixes = []
try:
    with open('prefixes.txt', 'r', encoding='utf-16-le') as f:
        prefixes = [line.strip() for line in f if line.strip()]
    print(f"Read {len(prefixes)} prefixes (UTF-16LE)")
except Exception as e:
    print(f"Error reading UTF-16LE: {e}")
    try:
        with open('prefixes.txt', 'r', encoding='utf-8') as f:
            prefixes = [line.strip() for line in f if line.strip()]
        print(f"Read {len(prefixes)} prefixes (UTF-8)")
    except Exception as e2:
        print(f"Error reading UTF-8: {e2}")

specialized = {'Account', 'Array', 'Check', 'Math', 'Object', 'String', 'Text'}
general_prefixes = sorted(list(set([p for p in prefixes if p not in specialized])))
print(f"General prefixes count: {len(general_prefixes)}")

# Construct generic regex
# Escape special regex chars if any (none expected in this list but good practice)
general_regex = '|'.join(map(re.escape, general_prefixes))
general_pattern = f"\\\\b({general_regex})[A-Z0-9_]\\\\w*\\\\b"

# Construct specialized patterns
specialized_patterns = {
    'support.function.array.mql5': "\\\\bArray[A-Z0-9_]\\\\w*\\\\b",
    'support.function.account-info.mql5': "\\\\bAccount[A-Z0-9_]\\\\w*\\\\b",
    'support.function.check.mql5': "\\\\bCheck[A-Z0-9_]\\\\w*\\\\b",
    'support.function.math.mql5': "\\\\bMath[A-Z0-9_]\\\\w*\\\\b",
    'support.function.object.mql5': "\\\\bObject[A-Z0-9_]\\\\w*\\\\b",
    'support.function.string.mql5': "\\\\bString[A-Z0-9_]\\\\w*\\\\b",
    'support.function.text.mql5': "\\\\bText[A-Z0-9_]\\\\w*\\\\b"
}

# Read grammar file
grammar_path = 'syntaxes/mql5.tmLanguage.json'
try:
    with open(grammar_path, 'r', encoding='utf-8') as f:
        grammar = json.load(f)
    print("Read grammar file")
except Exception as e:
    print(f"Error reading grammar: {e}")
    sys.exit(1)

# Update patterns
patterns = grammar.get('patterns', [])
print(f"Found {len(patterns)} patterns")

# Helper function to recursively find and update patterns
def update_patterns(patterns_list):
    count = 0
    for pattern in patterns_list:
        name = pattern.get('name')
        if name == 'support.function.prefix.mql5':
            pattern['match'] = general_pattern
            print(f"Updated {name}")
            count += 1
        elif name in specialized_patterns:
            pattern['match'] = specialized_patterns[name]
            print(f"Updated {name}")
            count += 1
        
        # Check nested patterns if any (though usually scopes are leaf nodes for match rules)
        if 'patterns' in pattern:
            count += update_patterns(pattern['patterns'])
    return count

# Also check repository patterns if any
if 'repository' in grammar:
    for repo_key in grammar['repository']:
        repo_item = grammar['repository'][repo_key]
        if 'patterns' in repo_item:
            updated_count_repo = update_patterns(repo_item['patterns'])
            print(f"Updated {updated_count_repo} patterns in repository.{repo_key}")

updated_count = update_patterns(patterns)
print(f"Total updated patterns: {updated_count}")

# Write back
try:
    with open(grammar_path, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=4)
    print("Wrote grammar file")
except Exception as e:
    print(f"Error writing grammar: {e}")
