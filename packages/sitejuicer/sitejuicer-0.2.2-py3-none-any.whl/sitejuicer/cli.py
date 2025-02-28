"""
Command-line interface for SiteJuicer
"""

import argparse
import sys
import os
import configparser
from pathlib import Path
from datetime import datetime

# Use proper absolute imports
from sitejuicer import __version__
from sitejuicer.core import (
    fetch_content, save_markdown, copy_to_clipboard,
    format_markdown, convert_to_html, convert_to_json,
    strip_jina_metadata
)


def save_api_key(api_key):
    """Save the API key to a configuration file."""
    config_dir = Path.home() / ".sitejuicer"
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "config.ini"
    
    config = configparser.ConfigParser()
    
    # Load existing config if it exists
    if config_file.exists():
        config.read(config_file)
    
    # Ensure the section exists
    if "api" not in config:
        config["api"] = {}
    
    # Update the API key
    config["api"]["jina_key"] = api_key
    
    # Save the config
    with open(config_file, "w") as f:
        config.write(f)
    
    # Set restrictive permissions on the config file
    os.chmod(config_file, 0o600)
    
    return str(config_file)


def get_api_key():
    """Retrieve the API key from the configuration file."""
    config_file = Path.home() / ".sitejuicer" / "config.ini"
    
    if not config_file.exists():
        return None
    
    config = configparser.ConfigParser()
    config.read(config_file)
    
    try:
        return config["api"]["jina_key"]
    except (KeyError, configparser.NoSectionError):
        return None


def main():
    """Main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Convert URLs to markdown using Jina Reader"
    )
    
    # Positional arguments should be defined first
    parser.add_argument("url", nargs="?", help="URL to convert to markdown")
    parser.add_argument("output_pos", nargs="?", help="Output filename (without extension)")
    
    # Optional arguments
    parser.add_argument("-o", "--output", help="Alternative way to specify output filename")
    parser.add_argument(
        "--version", action="store_true", help="Show version number and exit"
    )
    parser.add_argument(
        "--no-metadata", action="store_true", 
        help="Strip metadata headers (title, URL source) from output file"
    )
    
    # Add clipboard option
    parser.add_argument(
        "--clipboard", action="store_true",
        help="Copy content to clipboard instead of saving to file"
    )
    
    # API key management
    parser.add_argument(
        "--api", metavar="KEY", 
        help="Save a Jina Reader API key for use in future requests"
    )
    parser.add_argument(
        "--clear-api", action="store_true",
        help="Clear the saved Jina Reader API key"
    )
    
    # Content Filtering and Customization options
    content_group = parser.add_argument_group("Content Filtering")
    content_group.add_argument(
        "--include-elements", 
        help="Specify HTML elements to include (comma-separated, e.g., 'p,h1,h2,img')"
    )
    content_group.add_argument(
        "--exclude-elements", 
        help="Specify HTML elements to exclude (comma-separated, e.g., 'aside,nav,footer')"
    )
    content_group.add_argument(
        "--main-content-only", action="store_true",
        help="Extract only the main content, filtering out navigation, footers, etc."
    )
    
    # Output Format options
    format_group = parser.add_argument_group("Output Format")
    format_group.add_argument(
        "--format", choices=["markdown", "html", "json"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    format_group.add_argument(
        "--template", 
        help="Apply a template to the output (e.g., 'blog', 'docs', 'book')"
    )
    format_group.add_argument(
        "--include-images", action="store_true",
        help="Download and include images locally"
    )
    format_group.add_argument(
        "--image-dir", default="images/",
        help="Directory to store downloaded images (default: 'images/')"
    )
    
    args = parser.parse_args()
    
    # Show version and exit if requested
    if args.version:
        print(f"SiteJuicer {__version__}")
        return 0
    
    # Handle API key operations
    if args.api:
        config_path = save_api_key(args.api)
        print(f"API key saved to {config_path}")
        return 0
    
    if args.clear_api:
        config_path = save_api_key("")
        print(f"API key cleared from {config_path}")
        return 0
    
    # Check if URL is provided when needed for content fetching
    if not args.url and not (args.version or args.api or args.clear_api):
        parser.print_help()
        return 1
    
    # Get API key if available
    api_key = get_api_key()
    
    # Setup options dictionary to pass to fetch_content
    options = {
        "include_elements": args.include_elements.split(",") if args.include_elements else None,
        "exclude_elements": args.exclude_elements.split(",") if args.exclude_elements else None,
        "main_content_only": args.main_content_only,
        "output_format": args.format,
        "template": args.template,
        "include_images": args.include_images,
        "image_dir": args.image_dir or "images" if args.include_images else None,
        "api_key": api_key  # Pass the API key in the options
    }
    
    try:
        # Fetch content from URL with options
        result = fetch_content(args.url, options=options)
        
        # Generate filename if not provided
        # First check the flag, then the positional arg, then generate from title
        if args.output:
            filename = args.output
        elif args.output_pos:
            filename = args.output_pos
        else:
            # Use title or default to 'output'
            if result["title"]:
                # Clean title for filename
                filename = result["title"].lower().replace(" ", "_")
                filename = "".join(c for c in filename if c.isalnum() or c == "_")[:50]
            else:
                filename = "output"
        
        # Format content for output based on the specified format
        if args.format == "markdown":
            formatted_content = format_markdown(
                result["content"], 
                args.url, 
                result["title"], 
                not args.no_metadata
            )
        elif args.format == "html":
            formatted_content = convert_to_html(
                strip_jina_metadata(result["content"]) if args.no_metadata else result["content"]
            )
        elif args.format == "json":
            formatted_content = convert_to_json(
                strip_jina_metadata(result["content"]) if args.no_metadata else result["content"], 
                args.url, 
                result["title"]
            )
        else:
            formatted_content = result["content"]
        
        # Either save to file or copy to clipboard
        if args.clipboard:
            if copy_to_clipboard(formatted_content):
                print(f"Content copied to clipboard")
            else:
                print(f"Failed to copy to clipboard. Please install pyperclip with: pip install pyperclip", file=sys.stderr)
                return 1
        else:
            # Save markdown content
            output_path = save_markdown(
                result["content"], 
                filename, 
                args.url, 
                result["title"], 
                not args.no_metadata,
                output_format=args.format
            )
            
            print(f"Saved content to {output_path}")
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main()) 