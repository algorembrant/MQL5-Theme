
import json
import re

syntax_file = r'c:\Users\User\Desktop\VSCode\MQL5-Theme\syntax.md'
grammar_file = r'c:\Users\User\Desktop\VSCode\MQL5-Theme\syntaxes\mql5.tmLanguage.json'

# Mapping from syntax.md section headers to tmscope names
section_map = {
    "Preprocessor Directives": "keyword.other.preprocessor",
    "Data Types": "storage.type",
    "Control Flow Keywords": "keyword.control",
    "Storage Modifiers": "storage.modifier",
    "Trade Functions": "support.function.trade.mql5",
    "CTrade Class Methods": "support.function.ctrade.mql5",
    "Trade Request Actions (ENUM_TRADE_REQUEST_ACTIONS)": "support.constant.trade-action.mql5",
    "Order Type Constants (ENUM_ORDER_TYPE)": "support.constant.order-type.mql5",
    "Order State Constants (ENUM_ORDER_STATE)": "support.constant.order-state.mql5",
    "Order Filling Modes (ENUM_ORDER_TYPE_FILLING)": "support.constant.order-filling.mql5",
    "Order Time Types (ENUM_ORDER_TYPE_TIME)": "support.constant.order-time.mql5",
    "Position Constants (ENUM_POSITION_TYPE)": "support.constant.position-type.mql5",
    "Position Properties (ENUM_POSITION_PROPERTY_INTEGER/DOUBLE/STRING)": "support.constant.position-property.mql5",
    "Symbol ENUM Constants (ENUM_SYMBOL_INFO_...)": "support.constant.symbol-info.mql5",
    "Symbol Trade Modes (ENUM_SYMBOL_TRADE_MODE)": "support.constant.symbol-trade-mode.mql5",
    "Symbol Filling Modes (ENUM_SYMBOL_FILLING_MODE)": "support.constant.symbol-filling.mql5",
    "Account ENUM Constants (ENUM_ACCOUNT_INFO_...)": "support.constant.account-info.mql5",
    "Account Trade Modes (ENUM_ACCOUNT_TRADE_MODE)": "support.constant.account-trade-mode.mql5",
    "Account Stop Out Modes (ENUM_ACCOUNT_STOPOUT_MODE)": "support.constant.account-stopout.mql5",
    "Deal Constants (ENUM_DEAL_...)": "support.constant.deal.mql5",
    "Timeseries Functions": "support.function.timeseries.mql5",
    "Timeframe Constants (ENUM_TIMEFRAMES)": "support.constant.timeframe.mql5",
    "Symbol/Market Info Functions": "support.function.symbol-info.mql5",
    "Account Info Functions": "support.function.account-info.mql5",
    "Common Functions": "support.function.common.mql5",
    "Conversion Functions": "support.function.conversion.mql5",
    "String Functions": "support.function.string.mql5",
    "Array Functions": "support.function.array.mql5",
    "Math Functions": "support.function.math.mql5",
    "File Functions": "support.function.file.mql5",
    "MQL5 Structures": "support.type.struct.mql5",
    "Standard Library Classes": "support.class.stdlib.mql5",
    "Magic/Predefined Variables": "support.variable.predefined.mql5",
    "Event Handler Functions": "support.function.event.mql5",
    "Return Codes (ENUM_INIT_RETCODE)": "support.constant.init-retcode.mql5",
    "Terminal/Environment Constants": "support.constant.terminal.mql5",
    "Object Property Constants (OBJPROP_...)": "support.constant.objprop.mql5",
    "Boolean Constants": "constant.language.boolean",
    "Numeric Limits": "support.constant.numeric-limits.mql5",
    "Color Constants": "support.constant.color.mql5",
    "Chart Constants (ENUM_CHART_...)": "support.constant.chart.mql5",
    "Object Types (ENUM_OBJECT)": "support.constant.object-type.mql5",
    "Indicator Functions": "support.function.indicator.mql5",
    "Date and Time": "support.function.datetime.mql5",
    "Chart Functions": "support.function.chart.mql5",
    "Object Functions": "support.function.object.mql5",
    "Text Functions": "support.function.text.mql5",
    "Global Variables": "support.function.global-variable.mql5",
    "Custom Indicators": "support.function.custom-indicator.mql5",
    "Signal Functions": "support.function.signal.mql5",
    "Market Info Functions": "support.function.market-info.mql5",
    "Check Functions": "support.function.check.mql5",
    "Uncategorized": "support.function.uncategorized.mql5"
}

# The manually defined patterns that don't follow the simple word list structure
manual_patterns = [
    {
        "begin": "//",
        "end": "$",
        "name": "comment.line.double-slash.mql5"
    },
    {
        "begin": "/\\*",
        "end": "\\*/",
        "name": "comment.block.mql5"
    },
    {
        "begin": "\"",
        "end": "\"",
        "name": "string.quoted.double.mql5",
        "patterns": [
            {
                "match": "\\\\.",
                "name": "constant.character.escape.mql5"
            }
        ]
    },
    {
        "begin": "'",
        "end": "'",
        "name": "string.quoted.single.mql5",
        "patterns": [
            {
                "match": "\\\\.",
                "name": "constant.character.escape.mql5"
            }
        ]
    },
    {
        "match": "\\b\\d+(\\.\\d+)?\\b",
        "name": "constant.numeric.mql5"
    },
     {
        "match": "\\b(#define|#import|#include|#property|#resource)\\b",
        "name": "keyword.other.preprocessor"
    }
]

def parse_syntax_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = {}
    current_section = None
    
    # Split by lines
    lines = content.splitlines()
    
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith('## '):
            current_section = line[3:].strip()
            sections[current_section] = []
        elif line.startswith('```') or line == '':
            continue
        elif current_section:
            # Split by whitespace, these are the keywords
            keywords = line.split()
            sections[current_section].extend(keywords)
            
    return sections

def generate_grammar(sections):
    patterns = []
    
    # Add manual patterns first
    patterns.extend(manual_patterns)
    
    # Generate patterns from sections
    sorted_sections = sorted(list(sections.keys()))
    
    for section_name in sorted_sections: 
        if section_name not in section_map:
            print(f"Warning: Section '{section_name}' not mapped to a scope name. Skipping.")
            continue
            
        scope_name = section_map[section_name]
        keywords = sections[section_name]

        if not keywords:
            continue

        # Sort keywords by length descending to ensure longer matches are tried first (e.g. OrderSendAsync vs OrderSend)
        keywords.sort(key=len, reverse=True)
        
        # Escape special regex characters if any
        escaped_keywords = [re.escape(k) for k in keywords]
        
        # Create regex
        if section_name == "Preprocessor Directives":
             # Special handling for #
             regex = f"({'|'.join(escaped_keywords)})" 
        else:
            regex = f"\\b({'|'.join(escaped_keywords)})\\b"
        
        pattern = {
            "match": regex,
            "name": scope_name
        }
        patterns.append(pattern)
        
    final_patterns = patterns
    
    return {
        "$schema": "https://raw.githubusercontent.com/martinring/tmlanguage/master/tmlanguage.json",
        "name": "MQL5",
        "patterns": final_patterns,
        "scopeName": "source.mql5"
    }

def main():
    sections = parse_syntax_md(syntax_file)
    grammar = generate_grammar(sections)
    
    with open(grammar_file, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=4)
        
    print(f"Successfully generated {grammar_file} with {len(grammar['patterns'])} patterns.")

if __name__ == "__main__":
    main()
