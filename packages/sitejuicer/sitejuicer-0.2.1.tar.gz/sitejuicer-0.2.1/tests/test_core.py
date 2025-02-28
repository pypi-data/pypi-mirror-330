#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for the core module of SiteJuicer.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path to import SiteJuicer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import core


class TestCore(unittest.TestCase):
    """Test cases for the core module."""

    @patch('core.requests.get')
    def test_fetch_content(self, mock_get):
        """Test the fetch_content function."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '# Test Content\n\nThis is a test.'
        mock_get.return_value = mock_response

        # Call the function
        result = core.fetch_content('https://example.com', options={"api_key": "test_key"})

        # Assertions
        self.assertIsInstance(result, dict)
        self.assertIn('content', result)
        self.assertIn('url', result)
        self.assertEqual(result['url'], 'https://example.com')
        self.assertEqual(result['content'], '# Test Content\n\nThis is a test.')
        mock_get.assert_called_once()

    def test_format_markdown(self):
        """Test the format_markdown function."""
        content = '# Test Content\n\nThis is a test.'
        url = 'https://example.com'
        title = 'Test Title'

        # Test with metadata
        formatted = core.format_markdown(content, url, title, include_metadata=True)
        self.assertIn('# Test Title', formatted)
        self.assertIn('Source: https://example.com', formatted)
        self.assertIn('# Test Content', formatted)

        # Test without metadata
        formatted = core.format_markdown(content, url, title, include_metadata=False)
        self.assertNotIn('Source: https://example.com', formatted)
        self.assertEqual(formatted, content)

    def test_add_table_of_contents(self):
        """Test the add_table_of_contents function."""
        content = '# Heading 1\n\nContent 1\n\n## Heading 2\n\nContent 2\n\n### Heading 3\n\nContent 3'
        result = core.add_table_of_contents(content)
        
        self.assertIn('## Table of Contents', result)
        self.assertIn('- [Heading 1](#heading-1)', result)
        self.assertIn('  - [Heading 2](#heading-2)', result)
        self.assertIn('    - [Heading 3](#heading-3)', result)

    @patch('core.re.findall')
    def test_add_link_section(self, mock_findall):
        """Test the add_link_section function."""
        mock_findall.return_value = [
            '[Link 1](https://example.com/1)',
            '[Link 2](https://example.com/2)'
        ]
        
        content = 'Some content with [links](https://example.com)'
        result = core.add_link_section(content)
        
        self.assertIn('## Links', result)
        self.assertIn('- [Link 1](https://example.com/1)', result)
        self.assertIn('- [Link 2](https://example.com/2)', result)

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_markdown(self, mock_open):
        """Test the save_markdown function."""
        content = '# Test Content\n\nThis is a test.'
        core.save_markdown(content, 'test.md', 'https://example.com', 'Test Title')
        mock_open.assert_called_once_with('test.md', 'w', encoding='utf-8')
        mock_open().write.assert_called_once()

    def test_filter_content(self):
        """Test the filter_content function."""
        html = """
        <html>
        <body>
            <nav>Navigation</nav>
            <main>
                <h1>Main Content</h1>
                <p>This is the main content</p>
            </main>
            <footer>Footer</footer>
        </body>
        </html>
        """
        
        # Test main content filtering
        filtered = core.filter_content(html, main_content_only=True)
        self.assertIn('<h1>Main Content</h1>', filtered)
        self.assertIn('<p>This is the main content</p>', filtered)
        self.assertNotIn('<nav>Navigation</nav>', filtered)
        self.assertNotIn('<footer>Footer</footer>', filtered)
        
        # Test include elements
        filtered = core.filter_content(html, include_elements=['h1'])
        self.assertIn('<h1>Main Content</h1>', filtered)
        self.assertNotIn('<p>This is the main content</p>', filtered)
        
        # Test exclude elements
        filtered = core.filter_content(html, exclude_elements=['p'])
        self.assertIn('<h1>Main Content</h1>', filtered)
        self.assertNotIn('<p>This is the main content</p>', filtered)


if __name__ == '__main__':
    unittest.main() 