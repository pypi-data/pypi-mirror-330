# Changelog

All notable changes to the charstyle library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-03-01

### Added
- New `tabled()` function for creating formatted tables with the following features:
  - Automatic column width calculation
  - Individual column styling
  - Header styling
  - Border customization
  - Row highlighting
  - Cell formatters for conditional styling
  - Different table styles (default, compact, thin)
  - Consistent alignment across rows
- Improved CLI with subcommand structure:
  - Default command shows a summary of available commands
  - `python -m charstyle styles` to display all text styles
  - `python -m charstyle tables` to display all table examples
  - `python -m charstyle tables [style]` to display a specific table style
  - `python -m charstyle icons` to display all available icons
  - `python -m charstyle icons [category]` to display icons from a specific category
- Enhanced styles display:
  - Shows Style enum names alongside examples for easier reference
  - Uses fixed-width formatting for better readability and alignment
  - Organizes styles with regular colors on the left and bright colors on the right
  - Optimized display of background colors with appropriate text length
  - Standardized section headers to match the tables display style
- Text alignment features with the new `Align` enum (LEFT, RIGHT, CENTER)
- Width parameter for fixed-width text formatting
- Custom fill character support for padding text
- Comprehensive documentation for alignment features
- Examples demonstrating alignment and formatting capabilities

### Changed
- Made Unicode borders the default table style
- Enhanced header styling in tables with bold, underlined text
- Improved table alignment logic for conditionally formatted content
- Added a new "thin" table style with no header separator
- Optimized data visualization examples with appropriate styling
- Standardized section headers in styles display to match tables display

### Removed
- Removed unused `border_char` parameter from the `tabled()` function

## [0.2.0] - 2025-02-28

### Added
- Pattern styling functions for complex text styling
- `styled_pattern` function for regex-based styling
- `styled_format` function for format string styling
- `styled_pattern_match` function for conditional styling
- `styled_split` function for delimiter-based styling
- Terminal icons support with the `Icon` enum
- Comprehensive documentation and examples

## [0.1.0] - 2025-02-15

### Added
- Initial release
- Basic text styling with ANSI escape sequences
- Foreground and background color support
- Text style support (bold, italic, underline, etc.)
- Style combination with tuples
- Color support detection
- Basic documentation and examples

[Unreleased]: https://github.com/joaompinto/charstyle/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/joaompinto/charstyle/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/joaompinto/charstyle/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/joaompinto/charstyle/releases/tag/v0.1.0
