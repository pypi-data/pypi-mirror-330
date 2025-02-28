#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example script demonstrating how to use SiteJuicer programmatically.
"""

import os
import sys
from datetime import datetime

# Add parent directory to path to import SiteJuicer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import (
    fetch_content, 
    format_markdown,
    save_markdown, 
    save_html, 
    save_json,
    filter_content,
    extract_images
)

def main():
    """
    Demonstrate how to use SiteJuicer's core functions programmatically.
    """
    print("SiteJuicer Programmatic Usage Example")
    print("=====================================")
    
    # Example URL
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    print(f"Fetching content from: {url}")
    
    # Fetch content
    result = fetch_content(url, options={"api_key": os.environ.get("JINA_API_KEY")})
    content = result.get("content", "")
    title = result.get("title", "")
    print(f"Title: {title}")
    print(f"Content size: {len(content)} characters")
    
    # Apply filtering
    print("\nApplying content filtering...")
    filtered_content = filter_content(
        content, 
        main_content_only=True,
        include_elements=["p", "h1", "h2", "h3", "ul", "ol", "li", "blockquote", "code"]
    )
    
    # Format as markdown
    print("\nFormatting as markdown...")
    markdown_content = format_markdown(
        filtered_content, 
        url, 
        title=title,
        include_metadata=True,
        generate_toc=True,
        extract_links=True
    )
    
    # Create output directory
    output_dir = "example_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract images (optional)
    print("\nExtracting images...")
    content_with_images = extract_images(filtered_content, output_dir)
    
    # Save in different formats
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save as markdown
    md_filename = os.path.join(output_dir, f"example_{timestamp}.md")
    save_markdown(
        markdown_content, 
        md_filename, 
        url, 
        title=title
    )
    print(f"Saved markdown to: {md_filename}")
    
    # Save as HTML
    html_filename = os.path.join(output_dir, f"example_{timestamp}.html")
    save_html(
        filtered_content, 
        html_filename, 
        url, 
        title=title
    )
    print(f"Saved HTML to: {html_filename}")
    
    # Save as JSON
    json_filename = os.path.join(output_dir, f"example_{timestamp}.json")
    save_json(
        filtered_content, 
        json_filename, 
        url, 
        title=title
    )
    print(f"Saved JSON to: {json_filename}")
    
    print("\nDone! Check the 'example_output' directory for the results.")

if __name__ == "__main__":
    main() 