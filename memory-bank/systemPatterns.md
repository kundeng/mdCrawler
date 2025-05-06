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
The project uses a thin entry point (main.py) that delegates to the core implementation in src/md_crawler.py, facilitating packaging as a distributable binary.

### 8. Scheduled Automation Pattern
The system implements a GitHub Actions workflow for automated, scheduled execution:
- Daily scheduled runs for documentation updates
- Manual trigger option for on-demand updates
- Automatic commit and push of generated documentation
- Configurable execution environment through GitHub Actions

### 9. Local Development Simulation Pattern
The system provides a local simulation environment for GitHub Actions:
- Local execution of workflows using nektos/act
- Command-line interface for workflow testing
- Docker-based simulation of GitHub Actions runners
- Configurable event triggers and workflow selection
- Environment file (.env) support for secrets management
- Automatic installation of required tools

### 10. Native Interface Integration Pattern
The system leverages GitHub's native interface for workflow monitoring and management:
- Documentation directs users to GitHub's existing workflow UI
- Utilizes GitHub's built-in monitoring and triggering capabilities
- Reduces implementation complexity and maintenance burden
- Ensures users have access to all GitHub Actions features
- Follows the principle of not reinventing existing functionality

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
The architecture supports multiple deployment options:
- Python package with virtual environment
- Standalone executable binary
- GitHub Actions workflow (implemented)
- Docker container
- GitHub's native interface for workflow monitoring

## Code Organization

### 1. Entry Point Structure
- **main.py**: Thin entry point with minimal logic
- **src/md_crawler.py**: Core implementation with enhanced features

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
- **.github/workflows/**: Directory for GitHub Actions workflow definitions
- **scripts/**: Directory for utility scripts like local GitHub Actions runner

## Data Flow

### Main Application Flow
1. **Input**: URL or configuration file (with environment variable support)
2. **Configuration Processing**: Load and merge configurations
3. **Link Discovery**: Extract all internal links from main page
4. **URL Filtering**: Apply include/exclude patterns from configuration
5. **Content Extraction**: Process each page with content filters
6. **Custom Cleaning**: Apply site-specific content cleaners if configured
7. **Markdown Generation**: Convert filtered content to Markdown
8. **Output**: Save Markdown files to organized directory structure

### GitHub Actions Local Runner Flow
1. **Input**: Command-line arguments specifying workflow and event type
2. **Tool Detection**: Check for nektos/act installation and install if needed
3. **Command Construction**: Build the act command with appropriate parameters
4. **Execution**: Run the GitHub Actions workflow locally using Docker
5. **Output**: Display workflow execution results

### GitHub Native Interface Flow
1. **Input**: User interactions with GitHub's web interface
2. **Authentication**: GitHub's built-in authentication system
3. **Workflow Management**: List, monitor, and trigger workflows through GitHub UI
4. **Notification**: GitHub's notification system for workflow status updates
5. **Output**: Display workflow status and results in GitHub's interface

## Last Updated
[2025-05-06 12:50:00] - Updated with simplified GitHub Actions approach