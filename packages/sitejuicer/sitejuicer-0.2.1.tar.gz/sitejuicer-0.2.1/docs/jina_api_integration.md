# Jina Reader API Integration

This document explains how SiteJuicer integrates with the Jina Reader API to fetch and process web content.

## API Overview

The Jina Reader API is a service that converts web pages to LLM-friendly formats, such as Markdown or plain text. It extracts the main content from web pages, removes clutter, and formats the content in a way that can be easily processed by language models or other text processing systems.

## How SiteJuicer Uses the API

SiteJuicer uses the Jina Reader API in the following ways:

1. **Endpoint Format**: The API is accessed via `https://r.jina.ai/{url}` where `{url}` is the URL-encoded address of the webpage to be processed.

2. **Authentication**: The API requires a valid API key in the format `Bearer jina_xxxxx...` in the Authorization header.

3. **Request Flow**:
   - When a URL is submitted for processing, SiteJuicer first attempts to use the Jina Reader API with the provided API key
   - If no API key is provided or if the API call fails, it falls back to the public service (which may have rate limits)
   - The response is processed according to user preferences (content format, image handling, etc.)

4. **Response Handling**: 
   - The API returns the processed content in the specified format (Markdown by default)
   - SiteJuicer extracts the title from the content and processes any images as needed
   - The processed content is returned as a dictionary with `content`, `title`, and `url` keys

## API Key Management

To use the Jina Reader API with higher rate limits and additional features:

1. Obtain an API key from Jina AI (see [Reader API documentation](https://jina.ai/reader/))
2. Configure the API key in one of the following ways:
   - Set it as an environment variable: `JINA_API_KEY=jina_xxxxx...`
   - Pass it directly to the `fetch_content` function: `options={"api_key": "jina_xxxxx..."}`
   - Configure it in the UI (for the Streamlit interface)

## API Parameters

The Jina Reader API supports several parameters that can be passed to customize the response:

- `mainContentOnly` (boolean): Extract only the main content of the page
- `includeElements` (comma-separated string): HTML elements to specifically include
- `excludeElements` (comma-separated string): HTML elements to exclude
- And others as documented in the official API documentation

## Example Usage

```python
from core import fetch_content

# Basic usage
result = fetch_content("https://example.com", options={"api_key": "jina_xxxxx..."})
content = result["content"]
title = result["title"]

# With additional options
result = fetch_content(
    "https://example.com", 
    options={
        "api_key": "jina_xxxxx...",
        "main_content_only": True,
        "include_images": True,
        "image_dir": "images",
        "content_format": "markdown"
    }
)
```

## Troubleshooting

If you encounter issues with the API:

1. Verify that your API key is correct and properly formatted (should start with `jina_`)
2. Check that the URL you're trying to process is accessible and not blocked by the target website
3. Ensure you're not exceeding the rate limits for the API
4. Check the response for error messages that might indicate specific issues

For more details, refer to the [official Jina Reader API documentation](https://jina.ai/reader/). 