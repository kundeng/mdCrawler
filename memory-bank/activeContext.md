# Active Context: mdCrawler

## Current Focus
- Project refactoring for improved modularity and distribution
- Setting up GitHub Actions support
- Preparing for Python-to-EXE packaging
- Testing and validating refactored code
- Memory bank maintenance

## Recent Changes
- [2025-05-06 16:25:00] - Fixed GitHub Actions workflow to install Playwright and show generated files
- [2025-05-06 16:20:00] - Fixed GitHub Actions workflow to properly use checkout action for local testing
- [2025-05-06 15:52:00] - Added container architecture flag for better compatibility across different systems
- [2025-05-06 15:43:00] - Simplified GitHub Actions local runner script based on official nektos/act documentation
- [2025-05-06 15:11:00] - Updated GitHub Actions local runner script with official nektos/act secrets handling
- [2025-05-06 15:10:00] - Added nektos/act documentation to the project using mdCrawler
- [2025-05-06 13:06:00] - Enhanced GitHub Actions local runner script with .env file support for secrets
- [2025-05-06 12:48:00] - Created GitHub Actions local runner script and updated documentation
- [2025-05-06 12:21:00] - Implemented GitHub Actions workflow for automated documentation updates
- [2025-05-06 11:51:00] - Refactored main.py to be a thin entry point
- [2025-05-06 11:50:00] - Set up Python virtual environment (.venv)
- [2025-05-06 11:49:00] - Installed project dependencies
- [2025-05-06 11:05:00] - Updated memory bank with project refactoring goals
- [2025-05-06 11:04:00] - Updated productContext.md with enhanced project goals
- [2025-05-06 10:52:00] - Created memory bank structure

## Current Refactoring Status
The project has been refactored with the following changes:
- Created enhanced `src/md_crawler.py` (renamed from src/main.py) with improved configuration handling
- Simplified `main.py` to a minimal entry point that delegates to src/md_crawler.py
- Added support for URL pattern filtering in configuration
- Added support for custom content cleaners
- Enhanced configuration with environment variable support
- Set up Python virtual environment for isolation
- Successfully tested the refactored code with config/libraries.yaml

## Open Questions/Issues
1. How to structure the project for Python-to-EXE packaging?
2. What's the optimal module structure for the refactored codebase?
3. How to handle virtual environment setup in a distributable package?
4. How to optimize crawler performance for large documentation sites?
5. What additional filtering options might be useful for specific documentation formats?

## Current Project Structure
```
mdCrawler/
├── .github/
│   └── workflows/
│       └── doc-crawler.yml  # GitHub Actions workflow for automated documentation updates
├── config/
│   ├── __init__.py
│   ├── libraries.yaml
│   └── cleaners/
│       └── __init__.py
├── docker/
│   ├── docker-compose.yml
│   └── Dockerfile
├── docs/
├── scripts/
│   └── run_actions_locally.sh  # Script for running GitHub Actions locally
├── src/
│   ├── config_loader.py
│   └── md_crawler.py  # Enhanced version with improved configuration (renamed from main.py)
├── memory-bank/
│   ├── productContext.md
│   ├── activeContext.md
│   ├── systemPatterns.md
│   ├── decisionLog.md
│   └── progress.md
├── .gitignore
├── main.py  # Simplified entry point that delegates to src/md_crawler.py
├── README_GITHUB_ACTIONS.md  # Documentation for GitHub Actions tools
├── readme.md
└── requirements.txt
```

## Key Files
- **main.py**: Simplified entry point that delegates to src/md_crawler.py
- **src/md_crawler.py**: Enhanced implementation with improved configuration handling
- **config/libraries.yaml**: Configuration for batch processing multiple documentation sites with URL pattern support
- **src/config_loader.py**: Handles loading and parsing configuration files
- **docker/**: Contains Docker configuration for containerized execution
- **.github/workflows/doc-crawler.yml**: GitHub Actions workflow for automated documentation updates
- **scripts/run_actions_locally.sh**: Script for running GitHub Actions workflows locally using nektos/act
- **README_GITHUB_ACTIONS.md**: Documentation for GitHub Actions tools and using GitHub's native interface

## Key Differences Between main.py and src/md_crawler.py
1. **Configuration Handling**: src/md_crawler.py adds support for:
   - URL pattern filtering (include/exclude patterns)
   - Custom content cleaners
   - Environment variable configuration
   - Default configuration that can be overridden
2. **Modularity**: src/md_crawler.py is designed to be part of a modular structure
3. **Extensibility**: src/md_crawler.py adds support for custom scraping strategies
4. **Responsibility**: main.py is now a thin entry point that delegates to src/md_crawler.py

## Next Steps
1. Set up project structure for Python-to-EXE packaging
2. Enhance documentation with setup and usage instructions
3. Add more pre-configured documentation sources to libraries.yaml
4. Implement additional content filtering options for specific documentation formats
5. Test the GitHub Actions workflow with real-world documentation sources

## Last Updated
[2025-05-06 12:49:00] - Updated with simplified GitHub Actions approach