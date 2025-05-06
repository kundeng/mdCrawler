# Decision Log: mdCrawler

This file tracks significant architectural and design decisions made during the development of mdCrawler.

## [2025-05-06 10:53:00] - Memory Bank Initialization

**Decision**: Create a memory bank structure to maintain project context and track development decisions.

**Rationale**: 
- Provides centralized documentation for project context
- Enables better tracking of architectural decisions
- Improves knowledge transfer between development sessions
- Facilitates AI assistant understanding of project structure and goals

**Implications**:
- Need to keep memory bank files updated as project evolves
- Requires consistent documentation practices

## [2025-05-06 10:53:00] - Initial Architecture Analysis

**Decision**: Document the existing architecture patterns identified in the codebase.

**Rationale**:
- Establishes baseline understanding of the system
- Identifies key patterns for future development
- Provides context for future architectural decisions

**Implications**:
- Need to validate patterns with further code exploration
- May need to refine as understanding of the system deepens

## [2025-05-06 10:53:00] - Identified Crawler Configuration Strategy

**Decision**: The system uses a dual-configuration approach for crawling: one configuration for link discovery and another for content extraction.

**Rationale**:
- Link discovery needs less restrictive filtering to find all relevant pages
- Content extraction needs more aggressive filtering to produce clean Markdown
- Separation allows optimizing each phase independently

**Implications**:
- More complex configuration management
- Need to ensure both configurations remain in sync for optimal results
- Provides flexibility for different documentation site structures

## [2025-05-06 10:53:00] - Timeout and Rate Limiting Implementation

**Decision**: Implement timeout limits and request delays in the crawler.

**Rationale**:
- Prevents infinite crawling of large documentation sites
- Shows respect for target servers by limiting request frequency
- Improves reliability by handling potential hanging requests

**Implications**:
- May not process all pages on very large documentation sites
- Slightly increased processing time due to delays
- More predictable and reliable operation

## [2025-05-06 11:07:00] - Project Refactoring for Modularity and Distribution

**Decision**: Refactor the project to improve modularity, with a thin entry point (main.py) that delegates to core implementation in src/main.py.

**Rationale**:
- Enables packaging the project as a distributable binary (Python to exe)
- Improves code organization and maintainability
- Facilitates future extensions and enhancements
- Supports multiple deployment options (package, binary, GitHub Actions, Docker)

**Implications**:
- Need to restructure existing code
- Must maintain backward compatibility for existing users
- Requires clear separation between entry point and implementation
- Documentation needs to be updated to reflect new structure

## [2025-05-06 11:07:00] - Enhanced Configuration System

**Decision**: Enhance the configuration system with environment variable support, default configurations, and URL pattern filtering.

**Rationale**:
- Provides more flexibility for different deployment scenarios
- Enables configuration through environment variables for CI/CD pipelines
- Allows for more precise control over which URLs are processed
- Supports custom content cleaning for specific documentation sites

**Implications**:
- More complex configuration handling logic
- Need to document new configuration options
- Backward compatibility considerations for existing configurations
- Testing required for different configuration scenarios

## [2025-05-06 11:07:00] - Plugin Architecture for Content Cleaners

**Decision**: Implement a plugin architecture for content cleaners that can be dynamically loaded.

**Rationale**:
- Allows for site-specific content cleaning without modifying core code
- Enables community contributions for specific documentation sites
- Improves extensibility of the system
- Keeps core code clean and focused

**Implications**:
- Need to implement dynamic module loading
- Requires documentation for plugin development
- Error handling for plugin failures
- Testing framework for plugins

## [2025-05-06 11:07:00] - GitHub Actions Integration

**Decision**: Support running the tool as part of GitHub Actions workflows with local testing via "act".

**Rationale**:
- Enables automated documentation updates
- Provides CI/CD integration for documentation maintenance
- Allows for scheduled updates of documentation
- Local testing improves development workflow

**Implications**:
- Need to create GitHub Actions workflow definitions
- Documentation for GitHub Actions setup
- Testing with "act" for local workflow validation
- Consideration of rate limits and timeouts in CI environment

## [2025-05-06 12:00:00] - Module Renaming and Minimal Entry Point

**Decision**: Rename src/main.py to src/md_crawler.py and further simplify the main.py entry point.

**Rationale**:
- More descriptive module name that reflects its purpose
- Minimal entry point better supports both library and executable use cases
- Clearer separation between interface and implementation
- Improves code organization and maintainability

**Implications**:
- Easier to package as both a library and an executable
- Clearer project structure for new contributors
- Reduced complexity in the entry point
- Better alignment with Python packaging best practices

## [2025-05-06 11:52:00] - Successful Implementation of Thin Entry Point

**Decision**: Implement the thin entry point pattern by refactoring main.py to delegate to src/main.py.

**Rationale**:
- Validates the modular architecture design
- Confirms backward compatibility is maintained
- Demonstrates the effectiveness of the refactoring approach
- Provides a foundation for further enhancements

**Implications**:
- Simplified maintenance of the entry point
- Clearer separation of concerns in the codebase
- Easier to extend functionality in src/main.py without affecting the CLI interface
- Better support for future packaging as a distributable binary

## [2025-05-06 12:22:00] - GitHub Actions Workflow Implementation

**Decision**: Implement a GitHub Actions workflow for automated documentation updates on a daily schedule.

**Rationale**:
- Enables automated, scheduled documentation updates without manual intervention
- Provides consistent, up-to-date documentation for project users
- Leverages GitHub's infrastructure for reliable execution
- Supports both scheduled runs and manual triggering when needed
- Automatically commits and pushes documentation changes to the repository

**Implications**:
- Documentation will be refreshed daily, ensuring it stays current
- Changes to documentation sources will be automatically reflected in the repository
- Reduces manual maintenance burden for documentation
- May require monitoring of GitHub Actions logs for potential issues
- Workflow can be extended for additional CI/CD tasks in the future
## [2025-05-06 12:49:00] - Simplified GitHub Actions Tooling Approach

**Decision**: Implement a local testing script for GitHub Actions and leverage GitHub's native interface for monitoring and triggering workflows.

**Rationale**:
- Local runner script enables testing workflows without pushing to GitHub
- GitHub's native interface already provides excellent workflow monitoring and triggering capabilities
- Simplifies the implementation by avoiding custom UI development
- Reduces maintenance burden by relying on GitHub's well-maintained interface
- Users are likely already familiar with GitHub's workflow interface

**Implications**:
- Requires nektos/act for local testing
- Documentation needs to provide clear instructions for using GitHub's native interface
- No need to manage token security for a custom interface
- Reduces complexity in the codebase
- Better alignment with standard GitHub Actions usage patterns
## [2025-05-06 16:25:00] - Fixed GitHub Actions Workflow for Local Testing

**Decision**: Update the GitHub Actions workflow to properly handle local testing with nektos/act.

**Rationale**:
- Discovered that nektos/act requires the checkout action to properly populate the workspace
- Identified that Playwright needs to be installed in the container for the crawler to work
- Added a step to show the generated files for better visibility
- Removed unnecessary GitHub token guide that was not needed for the project

**Implications**:
- The workflow now works correctly in both local and GitHub environments
- The documentation crawler can now run successfully in the container
- Better visibility into the generated files
- Simplified project structure by removing unnecessary files
## [2025-05-06 15:53:00] - Added Container Architecture Flag for Compatibility

**Decision**: Add the `--container-architecture linux/amd64` flag to the GitHub Actions local testing script for better compatibility across different systems.

**Rationale**:
- Improves compatibility with Apple Silicon (M-series) Macs using Rosetta 2
- Addresses the warning message from nektos/act about potential issues on Apple M-series chips
- Provides a consistent environment for running GitHub Actions locally
- Aligns with the recommendation from nektos/act for Apple Silicon users
- Simplifies the script by using a consistent architecture regardless of the host system

**Implications**:
- Better compatibility across different systems, especially Apple Silicon Macs
- More reliable execution of GitHub Actions workflows locally
- Consistent behavior across different environments
- May slightly impact performance on non-x86 systems, but improves reliability
- Reduces troubleshooting needs for architecture-related issues
## [2025-05-06 15:48:00] - Added GitHub Token Guide for Local Testing

**Decision**: Create a comprehensive guide for generating GitHub tokens with minimum required permissions for local GitHub Actions testing.

**Rationale**:
- Local GitHub Actions testing requires authentication for accessing GitHub resources
- Users need clear guidance on creating tokens with appropriate permissions
- Minimum permissions principle is important for security
- Different workflows may require different token scopes
- Existing documentation lacked detailed instructions for token creation

**Implications**:
- Improved user experience for local GitHub Actions testing
- Enhanced security through guidance on minimum required permissions
- Better troubleshooting support for authentication issues
- More complete documentation for the GitHub Actions tooling
- Reduced friction for users trying to test workflows locally
## [2025-05-06 15:44:00] - Simplified GitHub Actions Local Testing Script

**Decision**: Simplify the GitHub Actions local testing script based on the official nektos/act documentation.

**Rationale**:
- The original script had unnecessary complexity and flags that weren't documented in the official nektos/act documentation
- Simplified command structure makes the script more maintainable and easier to understand
- Removed custom event file handling in favor of act's built-in event handling
- Aligned the script more closely with the official nektos/act usage patterns
- Used our own mdCrawler tool to fetch and analyze the official documentation

**Implications**:
- More reliable and maintainable script for local GitHub Actions testing
- Better alignment with official nektos/act usage patterns
- Reduced complexity makes the script easier to understand and modify
- Demonstrates the value of our mdCrawler tool for improving our own codebase
- Provides a better developer experience for local testing
## [2025-05-06 15:12:00] - Updated GitHub Actions Local Testing with Official Documentation

**Decision**: Update the GitHub Actions local testing script to use the official nektos/act methods for handling secrets and environment variables.

**Rationale**:
- Used our own mdCrawler tool to fetch and convert the official nektos/act documentation
- Discovered that our implementation was using custom methods instead of the official ones
- Official methods (`--secret-file` and `-s`) are more reliable and better maintained
- Documentation now includes advanced features like skipping jobs/steps during local testing
- Provides better alignment with the official nektos/act usage patterns

**Implications**:
- More reliable secrets handling for local GitHub Actions testing
- Better documentation for users based on official sources
- Demonstrates the value of our mdCrawler tool for maintaining up-to-date documentation
- Reduces maintenance burden by following official patterns
- Provides users with more advanced options for local testing
## [2025-05-06 13:07:00] - Environment File Support for Local GitHub Actions Testing

**Decision**: Enhance the local GitHub Actions testing script to support loading secrets from a .env file.

**Rationale**:
- GitHub Actions workflows often require secrets for authentication and API access
- Local testing with nektos/act needs a way to provide these secrets
- Environment files (.env) are a standard way to manage secrets in development
- Provides a consistent and secure way to manage secrets for local testing
- Simplifies the command-line interface by avoiding multiple --secret flags

**Implications**:
- Users need to create and manage a .env file for local testing
- Documentation needs to explain the format and usage of the .env file
- .env file must be added to .gitignore to prevent committing secrets
- Provides a more user-friendly experience for local workflow testing
- Enables testing of workflows that require authentication or API access
## Template for Future Entries

```
## [YYYY-MM-DD HH:MM:SS] - Decision Title

**Decision**: Brief description of the decision made.

**Rationale**:
- Reason 1
- Reason 2
- Reason 3

**Implications**:
- Implication 1
- Implication 2
- Implication 3
```