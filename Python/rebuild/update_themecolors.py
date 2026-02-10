import json
import os
import colorsys
import re
import random

# File paths
markdown_file_path = r"C:\Users\User\Desktop\VSCode\MQL5-Theme\syntax_List\grouping_syntaxes_cleaned.md"
dark_theme_path = r"C:\Users\User\Desktop\VSCode\MQL5-Theme\themes\mql5-syntax-dark.json"
light_theme_path = r"C:\Users\User\Desktop\VSCode\MQL5-Theme\themes\mql5-syntax-light.json"

# 1. Get all prefixes from MD
print(f"Reading {markdown_file_path}...")
with open(markdown_file_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

md_prefix_pattern = re.compile(r"that has '([^']+)' prefix")
md_prefixes = sorted(list(set(md_prefix_pattern.findall(md_content))))
print(f"Found {len(md_prefixes)} prefixes.")

# 2. Add alphabet fallback scopes
alphabet = "abcdefghijklmnopqrstuvwxyz"
fallback_scopes = [f"support.function.fallback.{char}.mql5" for char in alphabet]

# 3. Generate Colors
# We need distinct colors for each prefix group.
# A simple way is to generate colors around the hue wheel.
# We also need to be mindful of Light vs Dark themes.
# Dark theme: High brightness/saturation usually.
# Light theme: Lower brightness/darker colors usually.

def generate_colors(count, type="dark"):
    colors = []
    for i in range(count):
        hue = i / count
        if type == "dark":
            saturation = 0.7 + random.random() * 0.3 # 70-100%
            value = 0.8 + random.random() * 0.2      # 80-100%
        else:
            saturation = 0.6 + random.random() * 0.4 # 60-100%
            value = 0.4 + random.random() * 0.3      # 40-70% (darker)
        
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        hex_color = "#{:02x}{:02x}{:02x}".format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
        colors.append(hex_color)
    return colors

# Shuffle prefixes to mix them up or keep sorted?
# Users might associate similar prefixes with similar colors if sorted?
# But if we have 500 prefixes, neighbors will be very similar in hue.
# Random shuffling might be better for distinctness of neighbors.
# The user said "different colors individually".
# Let's shuffle the assignment to avoid rainbow gradients in sorted list which might look weird if not aligned with code usage.
# Actually, keeping them sorted might help finding them in the file, but color-wise, shuffling hue is better.
# Let's stick to a consistent hash-based or indexed color generation to be deterministic.

total_scopes = len(md_prefixes) + len(fallback_scopes)
dark_colors = generate_colors(total_scopes, "dark")
light_colors = generate_colors(total_scopes, "light")

# Create scope to color mapping
scope_color_map_dark = {}
scope_color_map_light = {}

# Assign for prefixes
for i, prefix in enumerate(md_prefixes):
    safe_name = re.sub(r'[^a-zA-Z0-9]', '-', prefix).lower()
    scope = f"support.function.prefix.{safe_name}.mql5"
    scope_color_map_dark[scope] = dark_colors[i]
    scope_color_map_light[scope] = light_colors[i]

# Assign for fallbacks
offset = len(md_prefixes)
for i, scope in enumerate(fallback_scopes):
    scope_color_map_dark[scope] = dark_colors[offset + i]
    scope_color_map_light[scope] = light_colors[offset + i]

# 4. Update Function
def update_theme_file(file_path, color_map, theme_type):
    print(f"Updating {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # We want to append these new rules.
    # Check if we should replace existing rules for these scopes?
    # To avoid duplicates, we can filter out existing rules that match these specific scopes.
    # But since these are new scopes (generated recently), they probably aren't in the theme file unless user added them.
    # Looking at file content, they are NOT there.
    
    # Create new tokenColors entries
    new_rules = []
    
    # We can group by color if we wanted to be efficient, but user wanted "individually".
    # Since we generated distinct colors (mostly), we'll add individual rules.
    # Note: 500+ rules in tokenColors is a lot but VS Code handles it.
    
    for scope, color in color_map.items():
        # Clean scope name for display
        # scope is support.function.prefix.something.mql5
        # name could be user friendly
        name_part = scope.split('.')[3] # prefix or fallback
        if "fallback" in scope:
             friendly_name = f"Fallback {name_part.upper()}"
        else:
             friendly_name = f"Prefix {name_part}"
             
        rule = {
            "name": friendly_name,
            "scope": scope,
            "settings": {
                "foreground": color
            }
        }
        new_rules.append(rule)
        
    # Append to tokenColors
    if "tokenColors" in data:
        data["tokenColors"].extend(new_rules)
    else:
        data["tokenColors"] = new_rules
        
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        
    print(f"Updated {file_path} with {len(new_rules)} new rules.")

# Execute updates
update_theme_file(dark_theme_path, scope_color_map_dark, "dark")
update_theme_file(light_theme_path, scope_color_map_light, "light")

print("Theme Update Complete.")
