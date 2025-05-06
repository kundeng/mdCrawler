# System Patterns: mdCrawler

## Architectural Patterns

### 1. Command-Line Interface Pattern
The application uses a command-line interface pattern with argparse to provide a flexible and user-friendly way to interact with the tool. This allows for both positional and named arguments, as well as configuration file support.

### 2. Configuration-Driven Architecture
The system uses YAML configuration files to define processing parameters, allowing for batch processing of multiple documentation sites without code changes. The refactored version enhances this with environment variable support and default configurations that can be overridden.

### 3. Asynchronous Processing
The crawler utilizes Python's asyncio for asynchronous processing, improving performance when crawling multiple pages.

### 4. Strategy Pattern
Different strategies are employed for content filtering and markdown generation, allowing for customization of the processing pipeline:
- `DefaultMarkdownGenerator` for converting HTML to Markdown
- `PruningContentFilter` for filtering out unwanted content
- Custom scraping strategies can be specified in configuration

### 5. Factory Pattern
The crawler creates and configures browser instances as needed, abstracting the complexity of browser automation.

### 6. Plugin Architecture
The refactored system implements a plugin architecture for content cleaners:
- Custom cleaner modules can be dynamically loaded from the `config/cleaners/` directory
- Cleaners are specified in the configuration and applied to the generated markdown

### 7. Entry Point Pattern
The project is being refactored to use a thin entry point (main.py) that delegates to the core implementation in src/main.py, facilitating packaging as a distributable binary.

## Design Principles

### 1. Separation of Concerns
- **Crawling Logic**: Handled by Crawl4AI
- **Content Processing**: Managed by filter strategies
- **Output Generation**: Handled by markdown generators
- **Configuration Management**: Separate from core logic
- **Entry Point**: Separated from implementation details

### 2. Configurability
The system is designed to be highly configurable, with options for:
- URL patterns to include/exclude
- Content filtering thresholds
- Output formatting options
- Browser configuration
- Custom content cleaners
- Environment variable overrides

### 3. Robustness
- Error handling for individual page failures
- Timeouts to prevent infinite crawling
- Rate limiting to be respectful to target servers
- Dynamic module loading with fallback mechanisms

### 4. Extensibility
The code structure allows for:
- Adding new filter strategies
- Supporting additional output formats
- Extending configuration options
- Customizing processing for specific documentation sites
- Adding custom content cleaners
- Implementing custom scraping strategies

### 5. Deployability
The refactored architecture supports multiple deployment options:
- Python package with virtual environment
- Standalone executable binary
- GitHub Actions workflow
- Docker container

## Code Organization

### 1. Entry Point Structure
- **main.py**: Thin entry point with minimal logic
- **src/main.py**: Core implementation with enhanced features

### 2. Configuration System
- **libraries.yaml**: Root configuration file
- **config/libraries.yaml**: Externalized configuration
- Environment variable support for configuration overrides
- Default configurations that can be merged with custom settings

### 3. Utility Functions
- URL processing and normalization
- Safe filename generation
- Link extraction and filtering
- Dynamic module loading

### 4. Core Processing Functions
- `crawl_documentation`: Process a single documentation site
- `crawl_multiple_libraries`: Process multiple sites from configuration
- Custom content cleaning via plugins

### 5. Extension Points
- **config/cleaners/**: Directory for custom content cleaner plugins
- Custom scraping strategies via configuration

## Data Flow

1. **Input**: URL or configuration file (with environment variable support)
2. **Configuration Processing**: Load and merge configurations
3. **Link Discovery**: Extract all internal links from main page
4. **URL Filtering**: Apply include/exclude patterns from configuration
5. **Content Extraction**: Process each page with content filters
6. **Custom Cleaning**: Apply site-specific content cleaners if configured
7. **Markdown Generation**: Convert filtered content to Markdown
8. **Output**: Save Markdown files to organized directory structure

## Last Updated
[2025-05-06 11:06:00] - Updated with refactored architecture patterns