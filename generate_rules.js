const fs = require('fs');
const path = require('path');

const grammarPath = './syntaxes/mql5.tmLanguage.json';
const grammar = JSON.parse(fs.readFileSync(grammarPath, 'utf8'));

// Extract all match patterns that have a 'name'
const scopes = new Set();

function extractScopes(obj) {
    if (obj.name) {
        scopes.add(obj.name);
    }
    if (obj.patterns) {
        obj.patterns.forEach(p => extractScopes(p));
    }
    if (obj.repository) {
        Object.values(obj.repository).forEach(r => extractScopes(r));
    }
}

extractScopes(grammar);

const sortedScopes = Array.from(scopes).sort();
const rules = [];

// Generate distinct colors (HSL)
function generateColor(index, total) {
    const hue = (index * 360 / total) % 360;
    return `hsl(${hue}, 70%, 45%)`; // Mid-tone for visibility in light/dark
}

function hslToHex(h, s, l) {
    l /= 100;
    const a = s * Math.min(l, 1 - l) / 100;
    const f = n => {
        const k = (n + h / 30) % 12;
        const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
        return Math.round(255 * color).toString(16).padStart(2, '0');
    };
    return `#${f(0)}${f(8)}${f(4)}`;
}

let colorIndex = 0;
const totalScopes = sortedScopes.length;

sortedScopes.forEach(scope => {
    // Skip fallback A-Z as we want specific colors for them, or handle them specially
    if (scope.includes('support.function.fallback.')) {
        // We will add these manually with specific colors
        return;
    }

    const hex = hslToHex((colorIndex * 137.508) % 360, 70, 45); // Golden angle approx for distribution
    colorIndex++;

    rules.push({
        name: scope,
        scope: scope,
        settings: {
            foreground: hex
        }
    });
});

// Add A-Z manual colors
const azColors = [
    "#D32F2F", "#388E3C", "#1976D2", "#F57C00", "#7B1FA2", "#0097A7", "#C2185B", "#827717",
    "#303F9F", "#E64A19", "#689F38", "#FF8F00", "#5D4037", "#455A64", "#E91E63", "#512DA8",
    "#0288D1", "#D81B60", "#00796B", "#F9A825", "#8E24AA", "#9E9D24", "#6D4C41", "#616161",
    "#7CB342", "#0277BD"
];
const letters = 'abcdefghijklmnopqrstuvwxyz'.split('');

letters.forEach((char, i) => {
    rules.push({
        name: `Unregistered Syntax ${char.toUpperCase()}`,
        scope: `support.function.fallback.${char}.mql5`,
        settings: {
            foreground: azColors[i]
        }
    });
});

console.log(JSON.stringify(rules, null, 4));
