# SiteJuicer Project Map

This document provides an overview of the SiteJuicer project structure, architecture, and functionality.

## Project Structure

```
SiteJuicer/
├── __init__.py                 # Package initialization, version info
├── __main__.py                 # Entry point for direct execution
├── cli.py                      # Command-line interface implementation
├── core.py                     # Core functionality
├── setup.py                    # Package setup and dependencies
├── README.md                   # Project documentation
├── LICENSE                     # License information
├── docs/                       # Documentation
│   ├── project-map.md          # This file
│   └── jina_api_integration.md # API integration documentation
├── examples/                   # Usage examples
│   └── usage_example.py        # Programmatic usage example
└── tests/                      # Test suite
    ├── __init__.py             # Test package initialization
    └── test_core.py            # Tests for core functionality
```

## Architecture

SiteJuicer follows a modular architecture with the following main components:

1. **Core Module (`core.py`)**: Contains the essential functionality for content fetching, processing, and saving.
2. **CLI Module (`cli.py`)**: Implements the command-line interface, argument parsing, and execution flow.

## Component Overview

### Core Module

The core module contains the fundamental functionality of SiteJuicer:

- `fetch_content()`: Fetches web content using the Jina Reader API, returning a dictionary with `content`, `title`, and `url` keys
- `filter_content()`: Filters HTML content based on specified elements
- `extract_images()`: Downloads images and updates references in the content
- `format_markdown()`: Formats content as markdown with various options
- `add_table_of_contents()`: Generates a table of contents from headings
- `add_link_section()`: Extracts and lists links from the content
- `save_markdown()`, `save_html()`, `save_json()`: Save content in various formats
- `cache_content()` and `get_cached_content()`: Handle content caching

### Jina Reader API Integration

The core module integrates with the Jina Reader API:

- **Endpoint Format**: `https://r.jina.ai/{url}`
- **Authentication**: Bearer token with the format `Bearer jina_XXXXX...`
- **Response Processing**: Handles JSON responses with content extraction
- **Error Handling**: Includes fallback to public service if API is unavailable
- **Option Handling**: Translates SiteJuicer options to appropriate API parameters

For detailed information about the API integration, see `docs/jina_api_integration.md`.

### CLI Module

The CLI module provides the command-line interface:

- `main()`: Entry point that parses arguments and dispatches to appropriate function
- `process_url()`: Processes a single URL and saves the result
- `process_batch()`: Processes multiple URLs from a batch file

## Flow Diagrams

### Single URL Processing Flow

```
User Input → CLI Arguments → process_url() → fetch_content() → 
    Extract content/title from result dictionary → filter_content() 
    → (optional) extract_images() → format_markdown()/HTML/JSON → save_XXX()
```

### Batch Processing Flow

```
Batch File → CLI Arguments → process_batch() → [For each URL] → process_url() 
    → Summarize Results
```

## Data Structures

### `fetch_content()` Return Structure

The `fetch_content()` function returns a dictionary with the following structure:

```python
{
    "content": str,  # The extracted content in the requested format
    "title": str,    # The title of the page
    "url": str       # The original URL that was processed
}
```

This dictionary is used throughout the application to pass content between components.

## Development Guidelines

### Adding New Features

1. Implement core functionality in `core.py`
2. Add CLI support in `cli.py`
3. Add tests in the `tests/` directory
4. Update documentation in `README.md` and `docs/`

### Dependency Management

- Core dependencies are listed in `setup.py` under `install_requires`
- Optional dependencies are listed under `extras_require` with keys:
  - `html`: Dependencies for HTML processing
  - `clipboard`: Dependencies for clipboard functionality
  - `all`: All optional dependencies

### Testing

- Run tests using `python -m unittest discover tests`
- Tests should cover core functionality, edge cases, and error handling

## Future Enhancements

- Advanced content filtering options
- Support for authentication-protected websites
- Batch processing with parallel execution
- Customizable templates for output formats
- Integration with other content extraction APIs
- Export to additional formats (PDF, ePub, etc.) 