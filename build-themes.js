const fs = require('fs');
const path = require('path');

// Paths
const VSCODE_DIR = __dirname;
const ROOT_DIR = VSCODE_DIR;
const SYNTAX_MD_PATH = path.join(VSCODE_DIR, 'syntax.md');
const CONFIG_PATH = path.join(VSCODE_DIR, 'syntax-colors.json');
const DARK_THEME_PATH = path.join(VSCODE_DIR, 'themes', 'mql5-syntax-dark.json');
const LIGHT_THEME_PATH = path.join(VSCODE_DIR, 'themes', 'mql5-syntax-light.json');
const SYNTAXES_DIR = path.join(ROOT_DIR, 'syntaxes');
const GRAMMAR_PATH = path.join(SYNTAXES_DIR, 'mql5.tmLanguage.json');


// Helper to read file content
function readFile(filePath) {
    try {
        return fs.readFileSync(filePath, 'utf8');
    } catch (err) {
        console.error(`Error reading ${filePath}:`, err.message);
        process.exit(1);
    }
}

// Helper to write JSON file
function writeJson(filePath, data) {
    try {
        const dir = path.dirname(filePath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
        fs.writeFileSync(filePath, JSON.stringify(data, null, 4));
        console.log(`Updated ${path.basename(filePath)}`);
    } catch (err) {
        console.error(`Error writing ${filePath}:`, err.message);
    }
}

// Parse syntax.md
function parseSyntaxMd(mdContent) {
    const lines = mdContent.split(/\r?\n/);
    const categories = {};
    let currentCategory = null;

    for (const line of lines) {
        // Detect Category Heading: ## Category Name
        const headingMatch = line.match(/^##\s+(.+)$/);
        if (headingMatch) {
            currentCategory = headingMatch[1].trim();
            categories[currentCategory] = new Set();
            continue;
        }

        // Detect keywords in code blocks or plain text
        // Skip empty lines, lines starting with ``` or ---
        if (!currentCategory || line.trim() === '' || line.startsWith('```') || line.startsWith('---') || line.startsWith('#')) {
            continue;
        }

        // Extract words separated by spaces (handling multiple spaces)
        // This regex splits by one or more whitespace characters
        const words = line.trim().split(/\s+/);
        for (const word of words) {
            if (word && word.length > 0) {
                categories[currentCategory].add(word);
            }
        }
    }

    // Convert Sets to Arrays
    for (const cat in categories) {
        categories[cat] = Array.from(categories[cat]);
    }

    return categories;
}

// Generate tokenColors for a specific theme type ('dark' or 'light')
function generateTokenColors(mdCategories, config, type) {
    const tokenColors = [];

    for (const [categoryName, categoryConfig] of Object.entries(config.categories)) {
        const color = type === 'dark' ? categoryConfig.darkColor : categoryConfig.lightColor;

        const settings = {
            foreground: color
        };

        if (categoryConfig.fontStyle) {
            settings.fontStyle = categoryConfig.fontStyle;
        }

        tokenColors.push({
            name: categoryName,
            scope: categoryConfig.scope,
            settings: settings
        });
    }

    // Add base/generic token colors defined in "baseTokenColors"
    if (config.baseTokenColors && config.baseTokenColors[type]) {
        const baseColors = config.baseTokenColors[type];
        const mapping = [
            { key: 'comments', scopes: ['comment', 'comment.line', 'comment.block', 'punctuation.definition.comment'] },
            { key: 'functions', scopes: ['entity.name.function', 'meta.function entity.name.function', 'support.function'] },
            { key: 'classes', scopes: ['entity.name.class', 'entity.name.type.class', 'entity.name.struct', 'entity.name.type.struct', 'support.class', 'support.type'] },
            { key: 'strings', scopes: ['string', 'string.quoted.double', 'string.quoted.single'] },
            { key: 'numbers', scopes: ['constant.numeric', 'constant.numeric.integer', 'constant.numeric.float', 'constant.numeric.decimal'] },
            { key: 'operators', scopes: ['keyword.operator', 'keyword.operator.arithmetic', 'keyword.operator.comparison', 'keyword.operator.logical', 'keyword.operator.assignment'] },
            { key: 'variables', scopes: ['variable', 'variable.other'] },
            { key: 'parameters', scopes: ['variable.parameter', 'variable.parameter.function'] },
            { key: 'includePaths', scopes: ['string.quoted.other.lt-gt', 'string.quoted.include', 'entity.name.other.preprocessor.macro.include'] },
            { key: 'punctuation', scopes: ['punctuation.definition.begin.bracket', 'punctuation.definition.end.bracket', 'punctuation.section.parens', 'punctuation.brackets', 'meta.brace', 'punctuation.separator', 'punctuation.terminator', 'punctuation.accessor'] },
            { key: 'enums', scopes: ['entity.name.type.enum', 'variable.other.enummember'] }
        ];

        const baseRules = mapping.map(item => {
            if (baseColors[item.key]) {
                const setting = baseColors[item.key];
                return {
                    name: item.key.charAt(0).toUpperCase() + item.key.slice(1),
                    scope: item.scopes,
                    settings: setting
                };
            }
            return null;
        }).filter(x => x !== null);

        // Prepend base rules
        return [...baseRules, ...tokenColors];
    }

    return tokenColors;
}

// Generate TextMate Grammar
function generateGrammar(mdCategories, config) {
    const repository = {};
    const patterns = [];

    // 1. Basic Standard Patterns (Comments, Strings, Numbers)
    // We add these first but usually grammar order matters: first match wins.
    // Actually comments and strings should typically be processed first so keywords inside strings aren't highlighted.

    // Comments
    patterns.push({
        "begin": "//",
        "end": "$",
        "name": "comment.line.double-slash.mql5"
    });
    patterns.push({
        "begin": "/\\*",
        "end": "\\*/",
        "name": "comment.block.mql5"
    });

    // Strings
    patterns.push({
        "begin": "\"",
        "end": "\"",
        "name": "string.quoted.double.mql5",
        "patterns": [{ "match": "\\\\.", "name": "constant.character.escape.mql5" }]
    });
    patterns.push({
        "begin": "'",
        "end": "'",
        "name": "string.quoted.single.mql5",
        "patterns": [{ "match": "\\\\.", "name": "constant.character.escape.mql5" }]
    });

    // Numbers (Simplified regex for integers and floats)
    patterns.push({
        "match": "\\b\\d+(\\.\\d+)?\\b",
        "name": "constant.numeric.mql5"
    });

    // 2. Generate Rules from syntax.md categories
    // Sort categories to ensure longer keywords match first? TextMate regex engine usually needs careful ordering.
    // But here we are matching exact IDs.

    for (const [categoryName, keywords] of Object.entries(mdCategories)) {
        if (!keywords || keywords.length === 0) continue;

        // Find corresponding scope in config
        const catConfig = config.categories[categoryName];
        if (!catConfig || !catConfig.scope || catConfig.scope.length === 0) continue;

        const scope = catConfig.scope[0]; // Use the first scope declared

        // Escape keywords for regex
        const escapedKeywords = keywords.map(w => w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));

        // Fix for Preprocessor Directives (starting with #)
        // \b matches between a word char (\w) and a non-word char (\W).
        // # is a non-word char. If preceded by space (non-word), \b won't match.
        // So for keywords starting with #, we shouldn't use the leading \b.
        let regexPattern;
        if (keywords.some(w => w.startsWith('#'))) {
            regexPattern = `(${escapedKeywords.join('|')})\\b`;
        } else {
            regexPattern = `\\b(${escapedKeywords.join('|')})\\b`;
        }

        patterns.push({
            "match": regexPattern,
            "name": scope
        });
    }

    return {
        "$schema": "https://raw.githubusercontent.com/martinring/tmlanguage/master/tmlanguage.json",
        "name": "MQL5",
        "patterns": patterns,
        "scopeName": "source.mql5"
    };
}

// Main Build Function
function build() {
    console.log('Starting theme build...');

    const mdContent = readFile(SYNTAX_MD_PATH);
    const config = JSON.parse(readFile(CONFIG_PATH));
    const mdCategories = parseSyntaxMd(mdContent);

    // Generate Grammar
    const grammar = generateGrammar(mdCategories, config);
    writeJson(GRAMMAR_PATH, grammar);

    const commonThemeSettings = {
        "$schema": "vscode://schemas/color-theme",
        "semanticHighlighting": true
    };

    // Syntax Only Theme (High Contrast / No UI Overrides)
    // We only provide tokenColors. We setting colors to {} means it inherits from user's current theme/defaults.
    // However, to make it a valid theme, we usually pick a "type" (dark/light).
    // To truly be "universal", we might need two files: MQL5 Syntax (Dark) and MQL5 Syntax (Light),
    // but they will NOT set editor.background.

    // Dark Syntax
    const darkTheme = {
        ...commonThemeSettings,
        "name": "MQL5 Syntax (Dark)",
        "type": "dark",
        "colors": {}, // No UI overrides
        "tokenColors": generateTokenColors(mdCategories, config, 'dark'),
        "semanticTokenColors": {}
    };

    // Light Syntax
    const lightTheme = {
        ...commonThemeSettings,
        "name": "MQL5 Syntax (Light)",
        "type": "light",
        "colors": {}, // No UI overrides
        "tokenColors": generateTokenColors(mdCategories, config, 'light'),
        "semanticTokenColors": {}
    };

    writeJson(path.join(VSCODE_DIR, 'themes', 'mql5-syntax-dark.json'), darkTheme);
    writeJson(path.join(VSCODE_DIR, 'themes', 'mql5-syntax-light.json'), lightTheme);

    console.log('Build complete.');
}

build();
