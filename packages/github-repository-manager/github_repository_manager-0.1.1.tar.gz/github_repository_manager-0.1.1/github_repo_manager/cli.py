#!/usr/bin/env python3
"""
Command line interface for GitHub Repository Manager
"""
import sys
import argparse
from github_repo_manager.core import GitHubRepoManager

def cli_main():
    parser = argparse.ArgumentParser(
        description="GitHub Repository Manager - Manage your GitHub repositories efficiently"
    )
    parser.add_argument("--token", help="GitHub personal access token")
    parser.add_argument("--username", help="GitHub username")
    parser.add_argument(
        "--pattern", 
        help="Filter repositories by name pattern (regex supported)"
    )
    parser.add_argument(
        "--visibility",
        choices=["public", "private", "all"],
        default="all",
        help="Filter repositories by visibility"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without making changes"
    )
    parser.add_argument(
        "--no-confirm",
        action="store_true",
        help="Skip confirmation prompts"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between operations in seconds"
    )

    args = parser.parse_args()

    try:
        # Initialize the manager with provided credentials
        manager = GitHubRepoManager(token=args.token, username=args.username)
        
        # Get repositories based on filters
        repos = manager.get_repositories(
            filter_pattern=args.pattern,
            visibility=args.visibility if args.visibility != "all" else None
        )
        
        # Process repositories with interactive selection and action choice
        action, count = manager.process_repositories(
            repos,
            dry_run=args.dry_run,
            confirm=not args.no_confirm,
            delay=args.delay
        )
            
    except ValueError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    cli_main()