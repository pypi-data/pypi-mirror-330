"""
Example of how to use SiteJuicer programmatically
"""

import os
from sitejuicer import extract_content, process_url, save_markdown

def main():
    # Example 1: Simple extraction
    url = "https://example.com"
    content = extract_content(url)
    print(f"Title: {content.get('title', 'No title')}")
    print(f"Content length: {len(content.get('markdown', ''))}")
    
    # Example 2: Process and save
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    result = process_url(
        url="https://news.ycombinator.com",
        include_images=True,
        include_links=True,
        generate_toc=True
    )
    
    if result:
        filepath = save_markdown(
            content=result,
            output_dir=output_dir,
            filename="hacker_news.md"
        )
        print(f"Saved to: {filepath}")
    
    # Example 3: Batch processing
    urls = [
        "https://github.com/blog",
        "https://python.org",
    ]
    
    for url in urls:
        print(f"Processing: {url}")
        result = process_url(url)
        if result:
            # Auto-generate filename from title
            save_markdown(result, output_dir)

if __name__ == "__main__":
    main() 