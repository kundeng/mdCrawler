# GitHub Actions Tools

This repository includes tools for working with GitHub Actions locally and guidance for using GitHub's native interface.

## Local GitHub Actions Runner

The `scripts/run_actions_locally.sh` script allows you to run GitHub Actions workflows locally using [nektos/act](https://github.com/nektos/act).

### Prerequisites

- Docker (required by nektos/act)
- Bash shell

### Installation

The script will automatically install `act` if it's not already installed:

- On macOS: Uses Homebrew to install `act`
- On Linux: Uses the official installation script

### Usage

```bash
# Run all workflows with default settings
./scripts/run_actions_locally.sh

# Run a specific workflow file
./scripts/run_actions_locally.sh -w doc-crawler.yml

# Trigger with a specific event type
./scripts/run_actions_locally.sh -e pull_request

# Show verbose output
./scripts/run_actions_locally.sh -v

# Show what would be executed without running it
./scripts/run_actions_locally.sh -d

# Show help
./scripts/run_actions_locally.sh -h
```

### Options

- `-w, --workflow FILE`: Specify workflow file to run (default: all workflows)
- `-e, --event TYPE`: Specify event type (default: workflow_dispatch)
- `-v, --verbose`: Enable verbose output
- `-d, --dry-run`: Show what would be executed without running it
- `-t, --token TOKEN`: GitHub token for authentication
- `-a, --actor NAME`: GitHub username for actions (default: github-actions)
- `-l, --local-actions`: Enable offline mode for actions (caches actions for faster execution)
- `-e, --env-file`: Path to .env file for secrets (default: .env)
- `-h, --help`: Show help message

### Limitations

When running GitHub Actions workflows locally with nektos/act, you may encounter some limitations:

1. **Authentication Issues**: By default, act doesn't have access to GitHub tokens, which can cause authentication failures when workflows try to access GitHub resources or use actions from the GitHub Marketplace. You can provide a GitHub token using the `-t` option, but some actions may still fail.

2. **Action Compatibility**: Not all GitHub Actions are compatible with act. Some actions may require specific GitHub runner features that aren't available in the local Docker environment.

3. **Secrets and Environment Variables**: You'll need to manually provide any secrets or environment variables that your workflow requires.

4. **GitHub Context**: Some GitHub context variables may not be available or may have different values when running locally.

5. **Architecture Compatibility**: Our script uses the `--container-architecture linux/amd64` flag for better compatibility across different systems, including Apple Silicon Macs with Rosetta 2.

To work around these limitations:

- Use the `-l` option to enable offline mode for actions
- Provide a GitHub token with the `-t` option
- Use a `.env` file to provide secrets (see below)
- Modify your workflows to be more compatible with local testing
- Consider using GitHub's native interface for full workflow testing

### Using Secrets with Local Testing

When running GitHub Actions workflows locally, you'll often need to provide secrets that would normally be available in the GitHub environment. The script supports loading secrets from a `.env` file:

1. Create a `.env` file in your project root (or specify a different location with `-e`)
2. Add your secrets in the format `KEY=VALUE`, one per line:

```
GITHUB_TOKEN=your_personal_access_token
API_KEY=your_api_key
DATABASE_PASSWORD=your_database_password
# You can also use export syntax
export MY_ENV='value'
# Multi-line values are supported
PRIV_KEY="---...\nrandom text\n...---"
JSON="{\n\"name\": \"value\"\n}"
```

3. Run the script with the `-e` option to specify your `.env` file:

```bash
./scripts/run_actions_locally.sh -w doc-crawler.yml -e .env
```

**Important**: Make sure to add `.env` to your `.gitignore` file to prevent committing secrets to your repository.

### GitHub Token

GitHub automatically provides a `GITHUB_TOKEN` secret when running workflows inside GitHub. If your workflow fails with an error about `token`, it most likely requires `GITHUB_TOKEN` to be set up. You can provide this token in several ways:

1. Using the `-t` option:
   ```bash
   ./scripts/run_actions_locally.sh -t your_github_token
   ```

2. In your `.env` file:
   ```
   GITHUB_TOKEN=your_github_token
   ```

3. If you have GitHub CLI installed, you can use:
   ```bash
   ./scripts/run_actions_locally.sh -t "$(gh auth token)"
   ```

For detailed instructions on creating a GitHub token with the minimum required permissions, see [GitHub Token Guide](docs/github_token_guide.md).

### Skipping Jobs or Steps

You can skip certain jobs or steps when running workflows locally:

1. To skip a job, add this condition to your workflow:
   ```yaml
   jobs:
     deploy:
       if: ${{ !github.event.act }} # skip during local actions testing
       runs-on: ubuntu-latest
       steps:
       - run: exit 0
   ```
   
   And create an event.json file with:
   ```json
   {
     "act": true
   }
   ```

2. To skip a step, use the `ACT` environment variable:
   ```yaml
   - name: Some step
     if: ${{ !env.ACT }}
     run: |
       ...
   ```

## Using GitHub's Native Interface

For monitoring and triggering workflows in production, we recommend using GitHub's native interface, which provides a comprehensive set of features for managing GitHub Actions.

### Accessing GitHub Actions

1. Navigate to your repository on GitHub
2. Click on the "Actions" tab at the top of the repository page
3. You'll see a list of all workflow runs for your repository

### Monitoring Workflow Runs

- The main Actions page shows all recent workflow runs
- Click on any run to see detailed information, including:
  - Step-by-step logs
  - Artifacts produced by the workflow
  - Timing information
  - Status of each job and step

### Triggering Workflows Manually

For workflows configured with the `workflow_dispatch` event (like our doc-crawler.yml):

1. Go to the Actions tab in your repository
2. In the left sidebar, click on the workflow you want to run
3. Click the "Run workflow" button
4. Select the branch to run the workflow on
5. Click "Run workflow" to start the execution

### Setting Up Scheduled Runs

Our documentation crawler workflow is configured to run on a schedule (daily at 2:00 UTC). You can view and modify this schedule in the workflow file:

```yaml
on:
  # Run on a schedule (every day at 2:00 UTC)
  schedule:
    - cron: '0 2 * * *'
  
  # Allow manual triggering
  workflow_dispatch:
```

The cron syntax follows the format: `minute hour day-of-month month day-of-week`

### Viewing Workflow Results

After a workflow completes:

1. You can see the updated documentation in the `docs/` directory
2. Any changes will be automatically committed and pushed to the repository
3. The commit history will show the automated updates with the message "Update documentation [automated]"

## Troubleshooting

### Local Runner Issues

- Make sure Docker is running
- Check that you have sufficient permissions to run Docker commands
- Verify that your workflow file is valid YAML

### GitHub Actions Issues

- Check the workflow logs for detailed error information
- Ensure your repository has the necessary permissions for the workflow
- For scheduled workflows that aren't running, check GitHub's status page for any service disruptions