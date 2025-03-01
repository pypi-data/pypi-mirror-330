# Changelog

All notable changes to SiteJuicer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.6] - 2025-03-03

### Added
- PyPI token management functionality for package publishing
- Commands to save, clear, and use PyPI tokens
- Feature to generate `.pypirc` file automatically from the saved token
- Cross-platform token handling with secure storage

## [0.2.5] - 2025-03-02

### Changed
- Improved cross-platform compatibility for Windows and macOS
- Made file permission handling compatible with Windows systems
- Updated package classifiers to explicitly indicate Windows and macOS support

## [0.2.4] - 2025-03-01

### Removed
- Removed clipboard functionality to simplify the codebase
- Removed clipboard-related dependencies (pyperclip and pywin32)
- Removed clipboard command-line option (--clipboard)
- Removed Windows-specific clipboard handling

## [0.2.3] - 2025-02-29

### Fixed
- Local Variable Access Error in Windows when using clipboard functionality
- Added Windows-specific clipboard handling with pywin32 fallback
- Improved clipboard initialization to prevent errors

### Added
- New optional dependencies: `clipboard` and `windows`
- Platform-specific documentation for Windows users
- Enhanced error handling for clipboard operations

## [0.2.2] - 2025-02-27

### Changed
- Updated README.md to focus on end-user experience
- Simplified installation instructions
- Improved documentation clarity
- Added automatic deployment to PyPI using GitHub Actions

### Added
- GitHub Actions workflow for automatic PyPI deployment on version tags
- Version consistency check for pull requests

## [0.5.0] - 2023-10-15

### Added
- Comprehensive Jina API authentication documentation
- New `jina_api_authentication.md` documentation file
- Validation for the new Jina API key format
- Warning messages for incorrectly formatted API keys
- Test script for verifying API key functionality

### Changed
- Updated `fetch_content` function to use Bearer token authentication
- Enhanced API key handling to support the new format (`jina_XXXXXXXXXXXXXXXXXXXXXXXX_XXXXXXXXXXXXXXXX`)
- Improved README with detailed API key setup instructions
- Updated programmatic usage examples with the new API key format

### Fixed
- Authentication issues with the Jina Reader API
- Error handling for API key validation

## [0.4.0] - 2023-09-25

### Added
- Detailed Jina Reader API integration documentation
- New `jina_api_integration.md` documentation file
- Support for newer Jina API key format (starting with `jina_`)
- Improved error handling for API responses

### Changed
- **Breaking**: Modified `fetch_content` to return a dictionary with `content`, `title`, and `url` keys
- Updated all references to `fetch_content` in CLI, UI, and examples
- Enhanced README with more detailed API integration information 
- Updated unit tests to reflect the new return structure

### Fixed
- API authentication issues with Jina Reader
- Error handling for failed API requests

## [0.3.0] - 2023-07-15

### Added
- Web UI mode with Streamlit interface
- Batch processing for multiple URLs
- Content filtering options (include/exclude elements)
- API server mode with FastAPI
- Comprehensive documentation
- Project structure map
- Developer guidelines and setup instructions
- Unit tests for core functionality
- Usage examples

### Changed
- Updated CLI interface with new command options
- Improved error handling and logging
- Enhanced README with detailed usage instructions
- Restructured project for better organization

## [0.2.1] - 2023-06-10

### Added
- Basic image extraction functionality
- Link extraction and formatting
- Table of contents generation

### Fixed
- URL validation issues
- Content parsing errors

## [0.2.0] - 2023-05-15

### Added
- Multiple output formats (Markdown, HTML, JSON)
- Metadata inclusion in output
- Command-line interface improvements

## [0.1.0] - 2023-04-01

### Added
- Initial release
- Basic web content extraction
- Markdown formatting
- Simple command-line interface 