const fs = require('fs');

const packagePath = './package.json';
const rulesPath = './key_rules_utf8.json';

const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
const rules = JSON.parse(fs.readFileSync(rulesPath, 'utf8').replace(/^\uFEFF/, ''));

// Update version
packageJson.version = "1.4.8";

// Update rules
if (!packageJson.contributes.configurationDefaults['[mql5]']) {
    console.error("Structure mismatch in package.json");
    process.exit(1);
}

packageJson.contributes.configurationDefaults['[mql5]']['editor.tokenColorCustomizations'].textMateRules = rules;

// Write back
fs.writeFileSync(packagePath, JSON.stringify(packageJson, null, 4));
console.log("Successfully updated package.json");
