#!/bin/bash
# Script to run GitHub Actions locally using nektos/act
# https://github.com/nektos/act

# Check if act is installed
if ! command -v act &> /dev/null; then
    echo "nektos/act is not installed. Installing now..."
    
    # Check OS and install accordingly
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install act
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
    else
        echo "Unsupported OS. Please install act manually from https://github.com/nektos/act"
        exit 1
    fi
fi

# Default values
WORKFLOW_FILE=""
EVENT_TYPE="workflow_dispatch"
VERBOSE=false
DRY_RUN=false
GITHUB_TOKEN=""
GITHUB_ACTOR="github-actions"
USE_LOCAL_ACTIONS=false
ENV_FILE=".env"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -w|--workflow)
            WORKFLOW_FILE="$2"
            shift
            shift
            ;;
        -e|--event)
            EVENT_TYPE="$2"
            shift
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -t|--token)
            GITHUB_TOKEN="$2"
            shift
            shift
            ;;
        -a|--actor)
            GITHUB_ACTOR="$2"
            shift
            shift
            ;;
        -l|--local-actions)
            USE_LOCAL_ACTIONS=true
            shift
            ;;
        -e|--env-file)
            ENV_FILE="$2"
            shift
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  -w, --workflow FILE    Specify workflow file to run (default: all workflows)"
            echo "  -e, --event TYPE       Specify event type (default: workflow_dispatch)"
            echo "  -v, --verbose          Enable verbose output"
            echo "  -d, --dry-run          Show what would be executed without running it"
            echo "  -t, --token TOKEN      GitHub token for authentication"
            echo "  -a, --actor NAME       GitHub username for actions (default: github-actions)"
            echo "  -l, --local-actions    Enable offline mode for actions (caches actions for faster execution)"
            echo "  -e, --env-file         Path to .env file for secrets (default: .env)"
            echo "  -h, --help             Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Build the command
CMD="act"

# Add event type
CMD="$CMD $EVENT_TYPE"

# Add workflow file if specified
if [ -n "$WORKFLOW_FILE" ]; then
    CMD="$CMD -W .github/workflows/$WORKFLOW_FILE"
fi

# Add job name
CMD="$CMD -j crawl-docs"

# Add GitHub token if provided
if [ -n "$GITHUB_TOKEN" ]; then
    CMD="$CMD -s GITHUB_TOKEN=$GITHUB_TOKEN"
fi

# Load secrets from .env file if it exists and not empty
if [ -f "$ENV_FILE" ] && [ -s "$ENV_FILE" ]; then
    echo "Loading secrets from $ENV_FILE"
    CMD="$CMD --secret-file $ENV_FILE"
else
    echo "No secrets file found or file is empty. Continuing without secrets."
fi

# Use local actions if specified
if [ "$USE_LOCAL_ACTIONS" = true ]; then
    CMD="$CMD --action-offline-mode"
fi

# Add verbose flag if specified
if [ "$VERBOSE" = true ]; then
    CMD="$CMD -v"
fi

# Always use linux/amd64 architecture for better compatibility
CMD="$CMD --container-architecture linux/amd64"

# Display the command
echo "Running: $CMD"

# Execute or dry run
if [ "$DRY_RUN" = true ]; then
    echo "Dry run - command would be: $CMD"
else
    eval $CMD
fi

echo "Done!"