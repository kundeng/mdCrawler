# Product Context: mdCrawler

## Project Overview
mdCrawler is a documentation-to-markdown converter tool designed to transform entire documentation websites into clean, organized collections of Markdown files. It's specifically optimized for providing context to AI coding assistants. The project is a fork with enhancements to improve modularity, configurability, and distribution options.

## Goals
1. Provide high-quality documentation context for AI coding assistants
2. Convert web-based documentation into accessible Markdown format
3. Preserve original documentation structure and organization
4. Support batch processing of multiple documentation sources
5. Create offline-accessible documentation for various use cases
6. Package as a distributable binary for easy installation
7. Support automation via GitHub Actions for regular documentation updates
8. Enable local testing of GitHub Actions workflows

## Features
1. **Automated Discovery**: Automatically discovers all documentation pages from a given URL
2. **Content Processing**: Downloads and processes each page with configurable filters
3. **Markdown Conversion**: Converts HTML content to clean Markdown format
4. **Structure Preservation**: Maintains the original documentation structure
5. **Batch Processing**: Supports processing multiple documentation sites via YAML configuration
6. **Customizable Filtering**: Provides options to filter content based on patterns and thresholds
7. **URL Pattern Filtering**: Supports include/exclude patterns for URL filtering
8. **Custom Content Cleaners**: Allows for site-specific content cleaning
9. **Environment Variable Configuration**: Supports configuration via environment variables

## Architecture
The system is built using Python with the following key components:

1. **Core Crawler**: Leverages Crawl4AI for web crawling capabilities
2. **Browser Automation**: Uses Playwright for browser-based content extraction
3. **Content Processing**: Implements filtering strategies to clean and format content
4. **Markdown Generation**: Converts processed content to well-structured Markdown
5. **Configuration System**: Supports YAML-based configuration for batch processing
6. **CLI Interface**: Provides command-line interface for easy usage
7. **Modular Structure**: Separates core functionality into src/ directory with main.py as entry point
8. **Extensible Cleaners**: Supports custom content cleaning modules in config/cleaners/

## Dependencies
- Crawl4AI: Core web crawling functionality
- Playwright: Browser automation for content extraction
- Python 3.8+: Base programming language
- YAML: Configuration file format
- Act (optional): For local testing of GitHub Actions workflows

## Deployment Options
1. **Python Package**: Run directly with Python in a virtual environment
2. **Executable Binary**: Packaged as a standalone executable
3. **GitHub Actions**: Run as part of automated workflows
4. **Docker Container**: Run in an isolated container environment

## Use Cases
1. Providing context to AI coding assistants
2. Offline documentation reading
3. Content migration projects
4. Documentation backups
5. Custom documentation styling
6. Automated documentation updates via CI/CD

## Project Status
Active development - Refactoring for improved modularity and distribution

## Last Updated
[2025-05-06 11:04:00] - Updated with project refactoring goals and enhanced features