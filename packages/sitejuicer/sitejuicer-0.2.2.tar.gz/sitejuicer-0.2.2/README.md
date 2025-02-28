# SiteJuicer 🧃

<div align="center">

![SiteJuicer Banner](docs/assets/sitejuicer-banner.jpg)

[![PyPI version](https://img.shields.io/pypi/v/sitejuicer.svg)](https://pypi.org/project/sitejuicer/)
[![Python Versions](https://img.shields.io/pypi/pyversions/sitejuicer.svg)](https://pypi.org/project/sitejuicer/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/sitejuicer)](https://pepy.tech/project/sitejuicer)

**Extract clean, readable content from any website with one command**

[Installation](#installation) • [Quick Start](#quick-start) • [Features](#features) • [Documentation](#documentation) • [Examples](#examples) • [Contributing](#contributing)

</div>

## 📖 Overview

SiteJuicer is a powerful command-line utility that converts web content to clean, readable formats like Markdown, HTML, and JSON using [Jina Reader](https://jina.ai/reader/). It helps extract valuable content from websites while removing clutter like ads, navigation menus, and other distractions.

> **Perfect for**: Content extraction, web scraping, research, offline reading, and data collection.

## ✨ Features

- 📝 **Clean content extraction** - Remove ads, navigation menus, and other distractions
- 🔄 **Multiple output formats** - Convert to Markdown, HTML, or JSON
- 🖼️ **Image extraction** - Download and save images from the page (optional)
- 🔗 **Link extraction** - Identify and list all links in the content (optional)
- 📚 **Table of contents** - Generate a TOC based on headings (optional)
- 📊 **Batch processing** - Process multiple URLs at once from a CSV or text file
- 🌐 **API server** - Run as a local API server with FastAPI
- 🖥️ **Web UI** - Use the graphical interface with Streamlit
- 🔑 **API Key Support** - Use your own Jina Reader API key for enhanced features

## 🚀 Quick Start

```bash
# Install
pip install sitejuicer

# Convert a URL to markdown (saved as {title}.md)
sitejuicer https://example.com

# Specify an output format
sitejuicer https://example.com --format html
```

## 📦 Installation

```bash
# Install from PyPI
pip install sitejuicer

# Optional UI components
pip install "sitejuicer[ui]"
```

### Installation with Optional Components

```bash
# For HTML conversion
pip install sitejuicer[html]

# For API server
pip install sitejuicer[server]

# For web UI
pip install sitejuicer[ui]

# For all features
pip install sitejuicer[all]
```

## 📋 Usage

### Basic Usage

```bash
# Convert a URL to markdown (output will be saved to {title}.md)
sitejuicer https://example.com

# Specify an output filename
sitejuicer https://example.com my-output

# Specify output format
sitejuicer https://example.com --format html
sitejuicer https://example.com --format json
```

### Using API Keys

```bash
# Save a Jina Reader API key for enhanced features
sitejuicer --api YOUR_API_KEY_HERE

# Clear a previously saved API key
sitejuicer --clear-api
```

When an API key is configured, SiteJuicer will automatically use it to access the Jina Reader API with enhanced features. If there's an issue with the API key, SiteJuicer will gracefully fall back to the public service.

API keys must be in the format `jina_XXXXXXXXXXXXXXXXXXXXXXXX_XXXXXXXXXXXXXXXX` and are stored securely at `~/.sitejuicer/config.ini` with restricted permissions.

### Output Format Options

```bash
# Apply a template to the output
sitejuicer https://example.com --template blog

# Download and include images locally
sitejuicer https://example.com --include-images

# Specify a directory for downloaded images
sitejuicer https://example.com --include-images --image-dir ./my-images
```

### Content Filtering Options

```bash
# Extract only the main content
sitejuicer https://example.com --main-content-only

# Include only specific HTML elements
sitejuicer https://example.com --include-elements p,h1,h2,h3,img

# Exclude specific HTML elements
sitejuicer https://example.com --exclude-elements aside,nav,footer
```

### Batch Processing

```bash
# Process URLs from a text file (one URL per line)
sitejuicer --batch urls.txt --output-dir ./converted

# Process URLs from a CSV file
sitejuicer --batch data.csv --output-dir ./converted
```

## 🌐 API Server Mode

```bash
# Start the API server on the default port (8000)
sitejuicer --server

# Start on a custom port
sitejuicer --server --port 5000
```

Once started, you can access the API documentation at `http://localhost:8000/docs`

## 🖥️ Web UI Mode

```bash
# Start the web UI
sitejuicer --ui
```

This will launch a Streamlit-based web interface at `http://localhost:8501`

## 🔄 How It Works

SiteJuicer uses the [Jina Reader API](https://jina.ai/reader/) to extract clean content from web pages. The processing pipeline includes:

1. Fetching the web content using the Jina Reader API
2. Optional content filtering to extract only the main content
3. Optional image downloading and reference updating
4. Optional link extraction and listing
5. Optional table of contents generation
6. Formatting and saving the content in the desired format (Markdown, HTML, or JSON)

## 🧩 Programmatic Usage

SiteJuicer can also be used programmatically in your Python scripts:

```python
from sitejuicer.core import fetch_content, format_markdown, save_markdown

# Fetch content from a URL with options
result = fetch_content(
    "https://example.com", 
    options={
        "main_content_only": True,
        "include_images": True,
        "image_dir": "images/",
        "api_key": "jina_2caa021406de46c7837bc05cce50e14d_qcv8AqU_xS_fCtKz3nJ2qS5IcDk"  # Optional: use your Jina Reader API key
    }
)

# Extract content and title from the result
content = result["content"]
title = result["title"]
url = result["url"]

# Format as markdown with options
markdown = format_markdown(
    content, 
    url=url, 
    title=title
)

# Save to a file with specific format
save_markdown(
    markdown, 
    "example.md", 
    url, 
    title, 
    output_format="markdown"
)
```

See the `examples/usage_example.py` file for a complete example.

## 🔌 API Integration

SiteJuicer integrates with the Jina Reader API to process web content. Key details:

- **Endpoint**: https://r.jina.ai/{url}
- **Authentication**: Bearer token with format `Bearer jina_XXXXXXXXXXXXXXXXXXXXXXXX_XXXXXXXXXXXXXXXX`
- **Response**: JSON object with processed content in requested format
- **Error Handling**: Graceful fallback to public service when API is unavailable or authentication fails

For detailed information about the API integration and authentication, see:
- [Jina API Integration](docs/jina_api_integration.md)
- [Jina API Authentication](docs/jina_api_authentication.md)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

<div align="center">
  
Created with ❤️ by [Jake Rains](https://github.com/jakerains)

If you find SiteJuicer useful, consider [starring the repository](https://github.com/jakerains/sitejuicer) or [buying me a coffee](https://ko-fi.com/jakerains).

</div> 