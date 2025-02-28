"""
SiteJuicer - utility to convert URLs to markdown using Jina Reader
"""

__version__ = '0.2.2'

# Import key functions for easier access
from sitejuicer.core import fetch_content, save_markdown
from sitejuicer.cli import main

# Define public API
__all__ = ['fetch_content', 'save_markdown', 'main'] 