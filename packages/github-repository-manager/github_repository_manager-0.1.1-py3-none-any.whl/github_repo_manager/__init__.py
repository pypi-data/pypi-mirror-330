"""
GitHub Repository Manager - A tool to interactively manage GitHub repositories
"""
from github_repo_manager.core import GitHubRepoManager
from github_repo_manager.cli import cli_main

__version__ = "0.1.2"
__all__ = ['GitHubRepoManager', 'cli_main']

if __name__ == "__main__":
    cli_main()