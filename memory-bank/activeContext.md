# Active Context: mdCrawler

## Current Focus
- Project refactoring for improved modularity and distribution
- Setting up GitHub Actions support
- Preparing for Python-to-EXE packaging
- Testing and validating refactored code
- Memory bank maintenance

## Recent Changes
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
2. What's the best approach for GitHub Actions integration?
3. How to implement local testing with the "act" library?
4. What's the optimal module structure for the refactored codebase?
5. How to handle virtual environment setup in a distributable package?
6. How to optimize crawler performance for large documentation sites?
7. What additional filtering options might be useful for specific documentation formats?

## Current Project Structure
```
mdCrawler/
├── config/
│   ├── __init__.py
│   ├── libraries.yaml
│   └── cleaners/
│       └── __init__.py
├── docker/
│   ├── docker-compose.yml
│   └── Dockerfile
├── docs/
├── src/
│   ├── config_loader.py
│   └── main.py  # Enhanced version with improved configuration
├── memory-bank/
│   ├── productContext.md
│   ├── activeContext.md
│   ├── systemPatterns.md
│   ├── decisionLog.md
│   └── progress.md
├── .gitignore
├── libraries.yaml
├── main.py  # Original entry point to be simplified
├── project.knowledge.md
├── readme.md
└── requirements.txt
```

## Key Files
- **main.py**: Current entry point that needs to be simplified to delegate to src/main.py
- **src/main.py**: Enhanced implementation with improved configuration handling
- **libraries.yaml**: Configuration for batch processing multiple documentation sites
- **config/libraries.yaml**: Externalized configuration with URL pattern support
- **src/config_loader.py**: Handles loading and parsing configuration files
- **docker/**: Contains Docker configuration for containerized execution

## Key Differences Between main.py and src/main.py
1. **Configuration Handling**: src/main.py adds support for:
   - URL pattern filtering (include/exclude patterns)
   - Custom content cleaners
   - Environment variable configuration
   - Default configuration that can be overridden
2. **Modularity**: src/main.py is designed to be part of a modular structure
3. **Extensibility**: src/main.py adds support for custom scraping strategies

## Next Steps
1. Simplify main.py to act as a thin entry point that delegates to src/main.py
2. Set up project structure for Python-to-EXE packaging
3. Implement GitHub Actions workflow
4. Add support for local testing with "act"
5. Enhance documentation with setup and usage instructions

## Last Updated
[2025-05-06 11:05:00] - Updated with project refactoring status