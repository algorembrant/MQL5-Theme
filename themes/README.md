# MQL5 Color Themes for VSCode / Antigravity

This folder contains custom color themes and file icons optimized for MQL5 (.mq5, .mqh) file development.

## File Icons

A custom MQL5 file icon extension has been installed to `%USERPROFILE%\.vscode\extensions\mql5-file-icons`.

**To activate the MQL5 file icons:**
1. Restart VSCode
2. Press `Ctrl+Shift+P` to open Command Palette
3. Type "File Icon Theme" and select "Preferences: File Icon Theme"
4. Select **"MQL5 File Icons"** from the list

## Included Themes

| Theme File | Type | Description |
|------------|------|-------------|
| `mql5-dark-theme.json` | Dark | Tokyo Night inspired dark theme with cyan, purple, and blue accents |
| `mql5-light-theme.json` | Light | One Light inspired theme with warm accents |

## Color Palette Reference

### Dark Theme Colors
- **Comments**: `#565f89` (gray, italic)
- **Preprocessor** (#property, #include): `#bb9af7` (purple)
- **Keywords** (if, for, return): `#bb9af7` (purple)
- **Types** (int, double, bool): `#2ac3de` (cyan)
- **Functions**: `#7aa2f7` (blue)
- **Strings**: `#9ece6a` (green)
- **Numbers**: `#ff9e64` (orange)
- **Variables**: `#c0caf5` (light blue)
- **Parameters**: `#e0af68` (gold, italic)
- **Class/Struct**: `#2ac3de` (cyan)
- **MQL5 Color Constants**: `#f7768e` (red)

## How to Use

### Method 1: Workspace Settings (Recommended - Already Configured)

The `.vscode/settings.json` file in this workspace already includes:
1. **File associations** - Maps `.mq5`, `.mqh`, `.mq4` files to C++ syntax
2. **Token color customizations** - Applies MQL5-specific highlighting to any theme

This method works immediately with any VSCode theme you currently use.

### Method 2: Install as Extension (For Full Theme Experience)

To use the complete dark or light themes:

1. **Quick Method - Copy to User Folder**:
   ```
   Copy the theme files to:
   Windows: %APPDATA%\Code\User\themes\
   ```

2. **Extension Method**:
   Create a folder structure for a VSCode extension:
   ```
   mql5-themes/
     package.json
     themes/
       mql5-dark-theme.json
       mql5-light-theme.json
   ```

   With this `package.json`:
   ```json
   {
     "name": "mql5-themes",
     "displayName": "MQL5 Color Themes",
     "version": "1.0.0",
     "engines": { "vscode": "^1.60.0" },
     "categories": ["Themes"],
     "contributes": {
       "themes": [
         {
           "label": "MQL5 Dark Professional",
           "uiTheme": "vs-dark",
           "path": "./themes/mql5-dark-theme.json"
         },
         {
           "label": "MQL5 Light Professional",
           "uiTheme": "vs",
           "path": "./themes/mql5-light-theme.json"
         }
       ]
     }
   }
   ```

3. Copy the folder to your VSCode extensions:
   ```
   Windows: %USERPROFILE%\.vscode\extensions\mql5-themes
   ```

4. Restart VSCode and select theme via `Ctrl+K Ctrl+T`

### Method 3: Direct Settings Override

Add to your user `settings.json`:
```json
{
  "workbench.colorTheme": "Default Dark+",
  "editor.tokenColorCustomizations": {
    "[Default Dark+]": {
      "textMateRules": [
        // Copy rules from mql5-dark-theme.json tokenColors array
      ]
    }
  }
}
```

## MQL5 Syntax Elements Highlighted

| Category | Examples |
|----------|----------|
| Preprocessor Directives | `#property`, `#include`, `#define`, `#import` |
| Input Parameters | `input double`, `input int`, `extern` |
| Data Types | `int`, `double`, `string`, `bool`, `datetime`, `color`, `ulong` |
| Control Flow | `if`, `else`, `for`, `while`, `return`, `break`, `switch` |
| Event Handlers | `OnInit()`, `OnTick()`, `OnDeinit()`, `OnTrade()`, `OnTimer()` |
| Trade Functions | `OrderSend()`, `PositionOpen()`, `PositionClose()` |
| CTrade Methods | `Buy()`, `Sell()`, `BuyLimit()`, `SellStop()` |
| Trade Action Constants | `TRADE_ACTION_DEAL`, `TRADE_ACTION_PENDING`, `TRADE_ACTION_SLTP` |
| Order Type Constants | `ORDER_TYPE_BUY`, `ORDER_TYPE_SELL`, `ORDER_TYPE_BUY_LIMIT` |
| Position Constants | `POSITION_TYPE_BUY`, `POSITION_TICKET`, `POSITION_PROFIT` |
| Symbol Constants | `SYMBOL_BID`, `SYMBOL_ASK`, `SYMBOL_TRADE_MODE_FULL` |
| Account Constants | `ACCOUNT_BALANCE`, `ACCOUNT_EQUITY`, `ACCOUNT_MARGIN_FREE` |
| Timeframe Constants | `PERIOD_M1`, `PERIOD_H1`, `PERIOD_D1`, `PERIOD_W1` |
| MQL5 Structures | `MqlRates`, `MqlTick`, `MqlTradeRequest`, `MqlTradeResult` |
| Standard Library | `CTrade`, `CPositionInfo`, `CSymbolInfo`, `CAccountInfo` |
| Timeseries Functions | `iTime()`, `iClose()`, `CopyRates()`, `CopySeries()` |
| Symbol Info Functions | `SymbolInfoDouble()`, `SymbolInfoInteger()` |
| Common Functions | `Print()`, `Alert()`, `Comment()`, `Sleep()` |
| Magic Variables | `_Symbol`, `_Digits`, `_Point`, `_Period`, `_LastError` |
| Color Constants | `clrRed`, `clrGreen`, `clrBlue`, `clrYellow` |

## Notes

- These themes are optimized for C++ syntax mode since VSCode treats `.mq5`/`.mqh` as C++
- Some MQL5-specific scopes may not be recognized if using a basic C++ grammar
- For best results, consider installing the "MQL5" extension from the VSCode marketplace if available
