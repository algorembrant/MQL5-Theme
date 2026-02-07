# MQL5 Support for VS Code

[![Open VSX Downloads](https://img.shields.io/open-vsx/dt/MQL5-Theme-syntax/mql5-support?label=Open%20VSX%20Downloads)](https://open-vsx.org/extension/MQL5-Theme-syntax/mql5-support)
[![Open VSX Version](https://img.shields.io/open-vsx/v/MQL5-Theme-syntax/mql5-support)](https://open-vsx.org/extension/MQL5-Theme-syntax/mql5-support)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Provide professional MQL5 (MetaQuotes Language 5) development support in Visual Studio Code.

## Features

- **Syntax Highlighting**: Comprehensive syntax highlighting for `.mq5` and `.mqh` files.

> **Note**: These are **Syntax-Only** color schemes. They do not change your workbench colors (sidebar, status bar, etc.), allowing you to keep your preferred UI aesthetics.

- **Extensive Coverage**: Supports `4,122 syntax definitions` extracted from the official 7,112-page [MQL5 Reference PDF](https://www.mql5.com/files/docs/mql5.pdf). These definitions were parsed from a 426,702-line [Markdown conversion](https://github.com/algorembrant/MQL5-Theme/blob/main/mql5.md) generated via [MarkItDown](https://github.com/microsoft/markitdown) using Python. *(Note: Do not worry, these large source files are used for development only and are not bundled with the extension).*

> [!CAUTION]
> **Disclaimer: Unofficial Extension**
> This extension is an independent open-source project and is **not** affiliated with, endorsed by, or connected to MetaQuotes Ltd.
> "MQL5", "MetaQuotes", and "MetaTrader" are registered trademarks of [MetaQuotes Ltd](https://www.metaquotes.net/).
> This extension is intended solely for syntax highlighting purposes to aid development.

## Syntax Support

Supports standard MQL5 types, functions, and constants defined in the [MQL5 Reference](https://www.mql5.com/en/docs).
See [Syntax Reference](https://github.com/algorembrant/MQL5-Theme/blob/main/syntax.md) for a detailed list of supported elements.

## References & Credits

All syntax definitions and language structures are based on the public [MQL5 Reference Manual](https://www.mql5.com/en/docs).
- **MQL5 Community**: [https://www.mql5.com/](https://www.mql5.com/)
- **Documentation**: [https://www.mql5.com/en/docs](https://www.mql5.com/en/docs)
- **Token Colors**: Inspired by standard MQL5 IDE colors.

## License

[MIT](LICENSE)
