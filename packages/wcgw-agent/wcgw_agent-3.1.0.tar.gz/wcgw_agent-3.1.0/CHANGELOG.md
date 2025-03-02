# Changelog

All notable changes to the WCGW project will be documented in this file.

## [3.1.0] - 2025-03-01

### Added
- **Windows Compatibility**: Added full support for Windows operating systems
  - Created platform_utils.py module for platform detection and abstraction
  - Implemented shell_handler.py with cross-platform shell handlers for both Windows and Unix
  - Developed windows_bg_process.py as a Windows alternative to the Unix 'screen' command
  - Added Windows-specific commands for background process management
  - Included Windows-specific setup instructions in documentation

### Changed
- **Package Name Change**: Renamed package from "wcgw" to "wcgw-agent" due to name conflict on PyPI
- Refactored the shell interaction system to be platform-agnostic
- Made pexpect a conditional dependency, only required for Unix-based systems
- Modified shell command execution to work across platforms
- Updated path handling to be compatible with Windows path conventions
- Improved error handling to be more robust across different operating systems
- Updated all installation instructions and command references to use the new package name

### Fixed
- Platform detection issues related to os.uname() on Windows
- Path separator inconsistencies between platforms
- Terminal attachment mechanism for interactive usage
- File opening functionality for Windows

## [3.0.6] - Previous Release

- See commit history for previous changes