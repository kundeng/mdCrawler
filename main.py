#!/usr/bin/env python3
"""
mdCrawler - Documentation to Markdown Converter

This is the main entry point for the mdCrawler tool. It provides a minimal
command-line interface and delegates all functionality to the implementation
in src/md_crawler.py.
"""

import sys

if __name__ == "__main__":
    # Import the main function from the core module
    from src.md_crawler import main
    
    # Execute the main function with the command-line arguments
    sys.exit(main())