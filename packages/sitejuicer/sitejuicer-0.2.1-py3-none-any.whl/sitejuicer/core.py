"""
Core functionality for SiteJuicer - fetching and processing content
"""

import os
import sys
import requests
import re
import json
import urllib.parse
from urllib.parse import quote, urljoin
from datetime import datetime

# Add pyperclip import for clipboard functionality
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


def fetch_content(url, options=None):
    """
    Fetch content from a URL using the Jina Reader API.
    
    Args:
        url (str): The URL to fetch content from.
        options (dict, optional): Options for the request. Defaults to None.
            - api_key (str): Jina Reader API key
            - main_content_only (bool): Extract only the main content
            - include_elements (list): HTML elements to include
            - exclude_elements (list): HTML elements to exclude
            - content_format (str): Format of the content ('markdown', 'text', 'html')
            - include_images (bool): Download and embed images
            - image_dir (str): Directory to save images
            - image_width (int): Width of embedded images
            
    Returns:
        dict: A dictionary containing the content and metadata.
    """
    if options is None:
        options = {}
    
    api_key = options.get("api_key")
    
    if api_key:
        # Use the correct Jina Reader API endpoint format
        jina_reader_url = f"https://r.jina.ai/{url}"
        
        # Update headers with the new API key format (Bearer token)
        headers = {}
        # Check if the API key has the correct format (starts with jina_)
        if api_key.startswith('jina_'):
            headers["Authorization"] = f"Bearer {api_key}"
        else:
            print(f"Warning: API key does not have the expected format (should start with 'jina_'). Authentication may fail.", file=sys.stderr)
            # Still try to use it as a Bearer token
            headers["Authorization"] = f"Bearer {api_key}"
        
        # Set query parameters if needed
        params = {}
        if options.get("main_content_only", False):
            params["mainContentOnly"] = "true"
        
        if options.get("include_elements"):
            params["includeElements"] = ",".join(options["include_elements"])
        
        if options.get("exclude_elements"):
            params["excludeElements"] = ",".join(options["exclude_elements"])
        
        try:
            # Use GET request as per the documentation
            response = requests.get(jina_reader_url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            content = response.text
            
            # Parse the response
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                # If not JSON, assume it's the raw content
                result = {
                    "content": content,
                    "title": url,
                    "url": url
                }
            
            # Process content based on format
            content_format = options.get("content_format", "markdown")
            if "content" in result and content_format.lower() in ["markdown", "text"]:
                result["content"] = _strip_metadata_headers(result["content"])
            
            # Download images if requested
            if options.get("include_images", False) and content_format.lower() == "markdown":
                result["content"] = download_images(
                    result["content"], 
                    url, 
                    result.get("title", url),
                    options.get("image_dir", "images")
                )
            
            return result
            
        except requests.RequestException as e:
            print(f"Error fetching content from Jina Reader API: {e}", file=sys.stderr)
            # Fall back to public service
    
    # Fallback to public service
    try:
        public_url = f"https://r.jina.ai/{url}"
        response = requests.get(public_url, timeout=30)
        response.raise_for_status()
        content = response.text
        
        # Extract title from the first # heading if possible
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        # Handle image downloading if requested
        if options.get("include_images", False):
            content = download_images(
                content, 
                url, 
                title,
                options.get("image_dir", "images")
            )
        
        return {
            "content": content,
            "title": title,
            "url": url,
        }
    except requests.RequestException as e:
        print(f"Error fetching content: {e}", file=sys.stderr)
        return {
            "content": "",
            "title": "",
            "url": url,
            "error": str(e)
        }


def download_images(content, base_url, title, image_dir):
    """
    Download images referenced in the markdown content and update links
    
    Args:
        content (str): The markdown content
        base_url (str): The base URL for resolving relative image paths
        title (str): The title to use in image naming
        image_dir (str): Directory to save images to
    
    Returns:
        str: Updated markdown with local image paths
    """
    # Create image directory if it doesn't exist
    title_slug = title.lower().replace(" ", "_")
    title_slug = "".join(c for c in title_slug if c.isalnum() or c == "_")[:50]
    
    img_dir = os.path.join(image_dir, title_slug)
    os.makedirs(img_dir, exist_ok=True)
    
    # Regular expression to find image links in markdown
    img_pattern = r'!\[(.*?)\]\((.*?)\)'
    
    def replace_image(match):
        alt_text = match.group(1)
        img_url = match.group(2)
        
        # Skip data URLs
        if img_url.startswith('data:'):
            return match.group(0)
        
        # Make sure url is absolute
        if not img_url.startswith(('http://', 'https://')):
            img_url = urljoin(base_url, img_url)
        
        # Create a filename for the image
        img_name = os.path.basename(urllib.parse.urlparse(img_url).path)
        if not img_name:
            img_name = f"image_{hash(img_url) % 10000}.jpg"
        
        img_path = os.path.join(img_dir, img_name)
        rel_path = os.path.join(image_dir, title_slug, img_name)
        
        try:
            # Download the image
            response = requests.get(img_url, timeout=10)
            with open(img_path, 'wb') as f:
                f.write(response.content)
            # Return markdown with local path
            return f'![{alt_text}]({rel_path.replace(os.sep, "/")})'
        except Exception as e:
            print(f"Warning: Failed to download image {img_url}: {e}", file=sys.stderr)
            return match.group(0)
    
    # Replace all image URLs with local paths
    return re.sub(img_pattern, replace_image, content)


def strip_jina_metadata(content):
    """
    Strip the metadata headers that Jina Reader adds to the content
    
    Args:
        content (str): The raw markdown content from Jina Reader
        
    Returns:
        str: The content without Jina Reader metadata
    """
    # Find where the actual markdown content starts
    match = re.search(r'Markdown Content:\s*\n', content)
    if match:
        # Return only the content after "Markdown Content:" line
        return content[match.end():]
    return content


def format_markdown(content, url, title=None, include_metadata=True):
    """
    Format markdown content with metadata headers
    
    Args:
        content (str): The raw markdown content
        url (str): The source URL
        title (str, optional): The title of the page
        include_metadata (bool): Whether to include metadata headers
        
    Returns:
        str: The formatted markdown content
    """
    # If no metadata is requested, strip Jina's metadata and return clean content
    if not include_metadata:
        return strip_jina_metadata(content)
        
    # Otherwise, keep the content as is (Jina already adds metadata)
    return content


def convert_to_html(markdown_content):
    """
    Convert markdown content to HTML
    
    Args:
        markdown_content (str): Markdown content
        
    Returns:
        str: HTML content
    """
    try:
        # Try to use commonmark for better compatibility
        import commonmark
        parser = commonmark.Parser()
        ast = parser.parse(markdown_content)
        renderer = commonmark.HtmlRenderer()
        return renderer.render(ast)
    except ImportError:
        # Fallback to simple HTML
        import html
        
        # Basic converter for demonstration
        lines = markdown_content.split('\n')
        html_lines = ['<!DOCTYPE html>', '<html>', '<head>', '<meta charset="utf-8">', 
                     f'<title>{html.escape(lines[0].strip("# "))}</title>', 
                     '<style>body{font-family:sans-serif;max-width:800px;margin:0 auto;padding:20px;line-height:1.6}</style>',
                     '</head>', '<body>']
        
        for line in lines:
            if line.startswith('# '):
                html_lines.append(f'<h1>{html.escape(line[2:])}</h1>')
            elif line.startswith('## '):
                html_lines.append(f'<h2>{html.escape(line[3:])}</h2>')
            elif line.startswith('### '):
                html_lines.append(f'<h3>{html.escape(line[4:])}</h3>')
            elif line.startswith('- '):
                html_lines.append(f'<li>{html.escape(line[2:])}</li>')
            elif line.strip() == '':
                html_lines.append('<br>')
            else:
                html_lines.append(f'<p>{html.escape(line)}</p>')
        
        html_lines.extend(['</body>', '</html>'])
        return '\n'.join(html_lines)


def convert_to_json(markdown_content, url, title):
    """
    Convert markdown content to JSON
    
    Args:
        markdown_content (str): Markdown content
        url (str): Source URL
        title (str): Title of the page
        
    Returns:
        str: JSON content
    """
    # Create a JSON structure with metadata and content
    data = {
        "title": title,
        "source_url": url,
        "date_extracted": datetime.now().isoformat(),
        "content": markdown_content,
        "sections": []
    }
    
    # Parse sections based on headings
    current_section = None
    current_content = []
    
    for line in markdown_content.split('\n'):
        if line.startswith('# '):
            # Level 1 heading - main title
            continue
        elif line.startswith('## '):
            # Save previous section if exists
            if current_section:
                data["sections"].append({
                    "title": current_section,
                    "content": '\n'.join(current_content)
                })
            
            # Start new section
            current_section = line[3:].strip()
            current_content = []
        elif line.startswith('### '):
            # Include subsection header in content
            current_content.append(f"Subsection: {line[4:].strip()}")
        else:
            if current_section:
                current_content.append(line)
    
    # Add the last section
    if current_section:
        data["sections"].append({
            "title": current_section,
            "content": '\n'.join(current_content)
        })
    
    return json.dumps(data, indent=2)


def save_markdown(content, filename, url, title=None, include_metadata=True, output_format="markdown"):
    """
    Save content to a file with proper formatting based on the specified output format
    
    Args:
        content (str): The content to save
        filename (str): The filename to save to (without extension)
        url (str): The source URL
        title (str, optional): The title of the page
        include_metadata (bool): Whether to include metadata headers
        output_format (str): The output format (markdown, html, json)
    
    Returns:
        str: The full path to the saved file
    """
    # Format the content according to the requested format
    if output_format == "markdown":
        formatted_content = format_markdown(content, url, title, include_metadata)
        extension = '.md'
    elif output_format == "html":
        # Convert to HTML
        formatted_content = convert_to_html(strip_jina_metadata(content) if not include_metadata else content)
        extension = '.html'
    elif output_format == "json":
        # Convert to JSON
        formatted_content = convert_to_json(strip_jina_metadata(content) if not include_metadata else content, url, title)
        extension = '.json'
    else:
        # Default to markdown
        formatted_content = format_markdown(content, url, title, include_metadata)
        extension = '.md'
    
    # Remove extension if present
    if filename.endswith('.md') or filename.endswith('.html') or filename.endswith('.json'):
        filename = os.path.splitext(filename)[0]
    
    # Add the appropriate extension
    output_filename = f"{filename}{extension}"
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        return os.path.abspath(output_filename)
    except IOError as e:
        print(f"Error saving file: {e}", file=sys.stderr)
        sys.exit(1)


def _strip_metadata_headers(content):
    """
    Strip metadata headers added by Jina Reader.
    
    Args:
        content (str): The content to process.
        
    Returns:
        str: The content without metadata headers.
    """
    lines = content.split('\n')
    metadata_section = False
    result_lines = []
    
    for line in lines:
        if line.startswith('---'):
            if not metadata_section:
                metadata_section = True
            else:
                metadata_section = False
            continue
            
        if not metadata_section:
            result_lines.append(line)
    
    return '\n'.join(result_lines)


def copy_to_clipboard(content):
    """
    Copy content to the system clipboard
    
    Args:
        content (str): The content to copy to clipboard
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not CLIPBOARD_AVAILABLE:
        print("Clipboard functionality requires pyperclip. Install with: pip install pyperclip", file=sys.stderr)
        return False
    
    try:
        pyperclip.copy(content)
        return True
    except Exception as e:
        print(f"Error copying to clipboard: {e}", file=sys.stderr)
        return False 