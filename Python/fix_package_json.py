
import json
import os

file_path = 'package.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Navigate to configurationDefaults
config_defaults = data.get('contributes', {}).get('configurationDefaults', {})

# Check if [mql5] exists
if '[mql5]' in config_defaults:
    mql5_config = config_defaults['[mql5]']
    if 'editor.tokenColorCustomizations' in mql5_config:
        # Move editor.tokenColorCustomizations to root of configurationDefaults
        config_defaults['editor.tokenColorCustomizations'] = mql5_config['editor.tokenColorCustomizations']
        # Remove [mql5]
        del config_defaults['[mql5]']
        print("Successfully moved editor.tokenColorCustomizations and removed [mql5] block.")
    else:
        print("[mql5] found but editor.tokenColorCustomizations not found inside it.")
else:
    print("[mql5] block not found in configurationDefaults. Already fixed?")

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
    print("package.json updated.")
