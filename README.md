# MQL5 Support for VS Code

[![Open VSX Downloads](https://img.shields.io/open-vsx/dt/MQL5-Theme-syntax/mql5-support?label=Open%20VSX%20Downloads)](https://open-vsx.org/extension/MQL5-Theme-syntax/mql5-support)
[![Open VSX Version](https://img.shields.io/open-vsx/v/MQL5-Theme-syntax/mql5-support)](https://open-vsx.org/extension/MQL5-Theme-syntax/mql5-support)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Provide professional MQL5 (MetaQuotes Language 5) development support in Visual Studio Code.

- **Extensive Coverage**: Supports `5,341+ syntax definitions` extracted from the official 7,112-page [MQL5 Reference PDF](https://www.mql5.com/files/docs/mql5.pdf). These definitions were parsed from a 426,702-line [Markdown conversion](https://github.com/algorembrant/MQL5-Theme/blob/main/mql5.md) generated via [MarkItDown](https://github.com/microsoft/markitdown) using Python. *(Note: Do not worry, these large source files are used for development only and are not bundled with the extension).*

## Features

- **Syntax Highlighting**: Comprehensive syntax highlighting for `.mq5` and `.mqh` files.
- **Enhanced Scoping**: Includes support for over **500+ specific MQL5 syntax groups**, each with distinct scopes based on prefixes (e.g., `Order...`, `Chart...`, `Math...`) allowing for granular theme customization.
- **Fallback Highlighting**: Intelligent fallback highlighting for identifiers starting with A-Z, ensuring every valid MQL5 token is colored even if not explicitly defined in a sub-group.
- **Refined Themes**: 
  - **MQL5 Syntax (Dark)**: High-contrast, vibrant colors optimized for dark environments.
  - **MQL5 Syntax (Light)**: Balanced, readable colors optimized for light environments.

> **Note**: These are **Syntax-Only** color schemes. They do not change your workbench colors (sidebar, status bar, etc.), allowing you to keep your preferred UI aesthetics.

> [!CAUTION]
> **Disclaimer: Unofficial Extension**
> This extension is an independent open-source project and is **not** affiliated with, endorsed by, or connected to MetaQuotes Ltd.
> "MQL5", "MetaQuotes", and "MetaTrader" are registered trademarks of [MetaQuotes Ltd](https://www.metaquotes.net/).
> This extension is intended solely for syntax highlighting purposes to aid development.

## References & Credits

All syntax definitions and language structures are based on the public [MQL5 Reference Manual](https://www.mql5.com/en/docs).
- **MQL5 Community**: [https://www.mql5.com/](https://www.mql5.com/)
- **Documentation**: [https://www.mql5.com/en/docs](https://www.mql5.com/en/docs)
- **Token Colors**: Inspired by standard MQL5 IDE colors but enhanced for modern VS Code capabilities.

## Support

If you find bugs or inconvenience, you may open an issue at the original [GitHub Repository](https://github.com/algorembrant/MQL5-Theme/issues) regarding on this MQL5 Support extension.

## License

[MIT](LICENSE)
