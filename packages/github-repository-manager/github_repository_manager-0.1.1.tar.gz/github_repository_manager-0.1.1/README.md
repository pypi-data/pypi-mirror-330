# GitHub Repository Manager

A command-line tool to interactively manage GitHub repositories with powerful features.

## Features

- Interactive terminal UI for managing repositories using arrow keys and spacebar
- Repository operations:
  - Archive repositories
  - Delete repositories
- Interactive action selection (choose between archive/delete after selecting repos)
- Pagination for large numbers of repositories
- Filter repositories by name pattern or visibility (public/private)
- Dry run mode to preview operations
- Confirmation step to prevent accidental operations
- Color-coded selection interface for easy navigation

## Installation

### Via pip (recommended)

```bash
pip install github-repository-manager
```

### Install from source

1. Clone this repository:

```bash
git clone https://github.com/conficiusa/github-repository-manager.git
cd github-repository-manager
```

2. Install the package:

```bash
pip install -e .
```

## Usage

### Command Line Interface

After installation, you can run the tool directly using:

```bash
github-repository-manager
```

Or with command line arguments:

```bash
github-repository-manager --pattern "test-" --dry-run
```

### Python Library

You can also use the package as a Python library in your code:

```python
# Using the convenience function
from github_repo_manager import manage_repositories

# Manage repositories interactively
manage_repositories(
    token="your-github-token",  # Optional: will prompt if not provided
    username="your-username",   # Optional: will prompt if not provided
    pattern="test-",           # Optional: filter repos by name
    visibility="private",      # Optional: 'public' or 'private'
    dry_run=True,             # Optional: preview without changes
    no_confirm=False,         # Optional: skip confirmation
    delay=1.0                 # Optional: delay between operations
)

# Using the class directly for more control
from github_repo_manager import GitHubRepoManager

# Initialize the manager
deleter = GitHubRepoManager(token="your-github-token", username="your-username")

# Get repositories (optionally filtered)
repos = deleter.get_repositories(filter_pattern="test-", visibility="private")

# Manage repositories with interactive selection
deleter.manage_repositories(repos, dry_run=True, confirm=True, delay=1.0)
```

### Authentication

The script will prompt you for:
- Your GitHub personal access token
- Your GitHub username

You can also provide these through:
- Command line arguments
- Environment variables (`GITHUB_TOKEN` and `GITHUB_USERNAME`)

### Command Line Arguments

```
usage: github-repository-manager [-h] [--token TOKEN] [--username USERNAME]
                           [--pattern PATTERN]
                           [--visibility {public,private}] [--no-confirm]
                           [--dry-run] [--delay DELAY]

Manage GitHub repositories

options:
  -h, --help            show this help message and exit
  --token TOKEN         GitHub personal access token
  --username USERNAME   GitHub username
  --pattern PATTERN     Regex pattern to match repository names
  --visibility {public,private}
                        Filter by visibility
  --no-confirm          Skip confirmation prompt
  --dry-run            Only show which repos would be affected
  --delay DELAY         Delay between operations in seconds
```

### Interactive UI Instructions

The script provides an interactive terminal UI for managing repositories:

1. **Repository Selection**:
   - Use ↑/↓ arrow keys to move between repositories
   - Press SPACE to select/unselect a repository
   - Use PgUp/PgDn to navigate between pages
   - Press `a` to select all repositories
   - Press `n` to clear all selections
   - Press ENTER to confirm selection
   - Press `q` to quit without changes

2. **Action Selection**:
   - After selecting repositories, choose between:
     - Archive: Archive the selected repositories
     - Delete: Delete the selected repositories
   - Use ↑/↓ arrow keys to select action
   - Press ENTER to confirm
   - Press `q` to cancel

3. **Confirmation**:
   - Review the selected repositories and action
   - Confirm with 'y' to proceed
   - Any other key to cancel

### Examples

1. Basic usage (will prompt for repository selection and action):
```bash
github-repository-manager
```

2. Manage only repositories matching a pattern:
```bash
github-repository-manager --pattern "test-"
```

3. Manage only private repositories:
```bash
github-repository-manager --visibility private
```

4. Dry run (preview only):
```bash
github-repository-manager --dry-run
```

5. Skip interactive selection:
```bash
github-repository-manager --no-confirm
```

## Creating a GitHub Personal Access Token

To use this script, you need a GitHub personal access token with appropriate scopes:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token" → "Generate new token (classic)"
3. Give your token a name and select the required scopes:
   - `repo` scope for both archiving and deleting repositories
   - `delete_repo` scope if you plan to delete repositories
4. Click "Generate token" and copy the token for use with this script

## Development

To contribute to the development of this tool:

1. Clone the repository
2. Install in development mode:
```bash
pip install -e .
```
3. Make your changes
4. Submit a pull request

## Publishing to PyPI

To publish this package to PyPI (for the maintainer):

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to PyPI (you'll need PyPI credentials)
twine upload dist/*
```

## Security Note

Never share your personal access token. The token grants access to your repositories, so handle it with care.

## License

This project is licensed under the MIT License - see the LICENSE file for details.