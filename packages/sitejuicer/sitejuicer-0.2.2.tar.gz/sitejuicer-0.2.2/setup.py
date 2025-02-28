from setuptools import setup, find_packages
import os
import re

# Read version from the package's __init__.py
with open('sitejuicer/__init__.py', 'r', encoding='utf-8') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        version = '0.2.1'  # Default version from __init__.py

# Read long description from README
try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Convert URLs to markdown using Jina Reader"

setup(
    name="sitejuicer",
    version=version,
    description="Convert URLs to markdown using Jina Reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jake Rains",
    author_email="your-email@example.com",
    url="https://github.com/jakerains/sitejuicer",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "sitejuicer=sitejuicer.cli:main",
        ],
    },
    install_requires=[
        "requests>=2.25.0",
        "rich>=12.0.0",
        "commonmark>=0.9.1",
        "typer>=0.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "mypy>=0.9.0",
            "flake8>=5.0.0",
        ],
        "ui": ["textual>=0.11.0"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    keywords="web scraping, markdown, url, jina, reader, sitejuicer",
) 