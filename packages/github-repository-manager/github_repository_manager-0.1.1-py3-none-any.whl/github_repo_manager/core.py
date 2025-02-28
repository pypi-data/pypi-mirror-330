"""
Core functionality for GitHub Repository Manager
"""
import requests
import os
import time
from blessed import Terminal

class GitHubRepoManager:
    def __init__(self, token=None, username=None):
        # Try getting token from environment variable first
        env_token = os.environ.get('GITHUB_TOKEN')
        
        if token:
            self.token = token
        elif env_token:
            self.token = env_token
        else:
            print("Please paste your GitHub personal access token (Right-click or Ctrl+V to paste):")
            self.token = input().strip()
        
        # Get username
        self.username = username or os.environ.get('GITHUB_USERNAME') or input("Enter your GitHub username: ").strip()
        print(f"Using account: {self.username}")
        
        # Configure API headers
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = 'https://api.github.com'
        self.term = Terminal()
        
    def get_repositories(self, filter_pattern=None, visibility=None, max_pages=10):
        """
        Get repositories matching criteria
        
        Args:
            filter_pattern (str, optional): Regex pattern to match repo names
            visibility (str, optional): Filter by visibility ('public', 'private', or None for all)
            max_pages (int, optional): Maximum number of pages to fetch (30 repos per page)
        
        Returns:
            list: List of repository objects
        """
        repos = []
        page = 1
        
        print(f"Fetching repositories for user {self.username}...")
        
        while page <= max_pages:
            # Fix the API parameters for visibility
            params = {'per_page': 30, 'page': page}
            if visibility:
                # The 'type' param is not correct for filtering by visibility
                # Use 'visibility' parameter instead
                params['visibility'] = visibility.lower()
                
            response = requests.get(
                f"{self.base_url}/user/repos", 
                headers=self.headers,
                params=params
            )
            
            if response.status_code != 200:
                print(f"Error fetching repositories: {response.status_code}")
                print(f"Response: {response.text}")
                print("Headers used:", self.headers)
                print("Params used:", params)
                print("Check your token has the necessary 'repo' scope permissions")
                break
                
            page_repos = response.json()
            if not page_repos:
                break
                
            repos.extend(page_repos)
            page += 1
            
        print(f"Found {len(repos)} repositories")
        
        # Filter by pattern if provided
        if filter_pattern:
            import re
            pattern = re.compile(filter_pattern)
            repos = [repo for repo in repos if pattern.search(repo['name'])]
            print(f"After filtering: {len(repos)} repositories match pattern '{filter_pattern}'")
            
        return repos
        
    def delete_repository(self, repo_name):
        """
        Delete a specific repository
        
        Args:
            repo_name (str): Name of the repository to delete
        
        Returns:
            bool: True if successful, False otherwise
        """
        url = f"{self.base_url}/repos/{self.username}/{repo_name}"
        response = requests.delete(url, headers=self.headers)
        
        if response.status_code == 204:
            print(f"Successfully deleted {repo_name}")
            return True
        else:
            print(f"Failed to delete {repo_name}: {response.status_code}")
            print(response.text)
            return False
            
    def archive_repository(self, repo_name):
        """
        Archive a specific repository
        
        Args:
            repo_name (str): Name of the repository to archive
        
        Returns:
            bool: True if successful, False otherwise
        """
        url = f"{self.base_url}/repos/{self.username}/{repo_name}"
        payload = {'archived': True}
        response = requests.patch(url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            print(f"Successfully archived {repo_name}")
            return True
        else:
            print(f"Failed to archive {repo_name}: {response.status_code}")
            print(response.text)
            return False

    def select_repositories_interactively(self, repos):
        """
        Interactive UI to select repositories using arrow keys and spacebar
        
        Args:
            repos (list): List of repository objects
        
        Returns:
            list: List of selected repositories
        """
        term = self.term
        selected = [False] * len(repos)
        current_pos = 0
        
        # How many repos to show at once
        page_size = min(15, term.height - 7)
        scroll_offset = 0
        
        # Define header_lines for formatting
        header_lines = 3  # Title + selection count + separator
        
        def draw_repo_line(idx, is_selected, is_current):
            """Helper to draw a repository line efficiently"""
            repo = repos[idx]
            line = f"[{idx+1}] {repo['name']} ({repo['visibility']})"
            
            if is_current and is_selected:
                return term.black_on_green(f"→ {line}")
            elif is_current:
                return term.black_on_white(f"→ {line}")
            elif is_selected:
                return term.green(f"  {line}")  # No arrow, just green text
            else:
                return f"  {line}"  # No arrow for unselected items
        
        def draw_screen():
            """Draw the entire screen with pagination"""
            visible_start = scroll_offset
            visible_end = min(scroll_offset + page_size, len(repos))
            
            with term.location(0, 0):
                print(term.clear)
                print(term.bold + "Select repositories (use arrow keys, SPACE to select, ENTER to confirm)" + term.normal)
                print(f"Selected: {selected.count(True)} of {len(repos)} | Page: {scroll_offset//page_size + 1}/{(len(repos)-1)//page_size + 1}")
                print("-" * term.width)
                
                # Print visible repositories with selection status
                for i in range(visible_start, visible_end):
                    print(draw_repo_line(i, selected[i], i == current_pos))
                
                # Fill remaining space with empty lines to maintain consistent UI
                for _ in range(visible_end - visible_start, page_size):
                    print()
                
                print("-" * term.width)
                print(f"↑/↓: Navigate | PgUp/PgDn: Page | SPACE: Select | A: Select All | N: Select None | ENTER: Confirm | Q: Quit")
        
        # Initial full draw
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            draw_screen()
            
            while True:
                # Get user input
                key = term.inkey()
                old_pos = current_pos
                old_scroll = scroll_offset
                need_full_redraw = False
                
                # Handle navigation keys
                if key.name == 'KEY_UP':
                    current_pos = max(0, current_pos - 1)
                    # Scroll up if needed
                    if current_pos < scroll_offset:
                        scroll_offset = current_pos
                        need_full_redraw = True
                elif key.name == 'KEY_DOWN':
                    current_pos = min(len(repos) - 1, current_pos + 1)
                    # Scroll down if needed
                    if current_pos >= scroll_offset + page_size:
                        scroll_offset = current_pos - page_size + 1
                        need_full_redraw = True
                elif key.name == 'KEY_PGUP':
                    # Move up a full page
                    current_pos = max(0, current_pos - page_size)
                    scroll_offset = max(0, scroll_offset - page_size)
                    need_full_redraw = True
                elif key.name == 'KEY_PGDOWN':
                    # Move down a full page
                    current_pos = min(len(repos) - 1, current_pos + page_size)
                    scroll_offset = min(len(repos) - page_size, scroll_offset + page_size)
                    if scroll_offset < 0:
                        scroll_offset = 0
                    need_full_redraw = True
                elif key.name == 'KEY_HOME':
                    current_pos = 0
                    scroll_offset = 0
                    need_full_redraw = True
                elif key.name == 'KEY_END':
                    current_pos = len(repos) - 1
                    scroll_offset = max(0, len(repos) - page_size)
                    need_full_redraw = True
                
                # Handle selection
                elif key == ' ':  # Spacebar
                    selected[current_pos] = not selected[current_pos]
                    # Update selection count
                    with term.location(0, 1):
                        print(term.clear_eol + f"Selected: {selected.count(True)} of {len(repos)} | Page: {scroll_offset//page_size + 1}/{(len(repos)-1)//page_size + 1}")
                
                # Select all/none actions require full redraw
                elif key == 'a':  # Select all
                    selected = [True] * len(repos)
                    need_full_redraw = True
                elif key == 'n':  # Select none
                    selected = [False] * len(repos)
                    need_full_redraw = True
                
                # Handle confirmation or quit
                elif key.name == 'KEY_ENTER':
                    break
                elif key == 'q':
                    return []
                
                # Redraw screen if needed
                if need_full_redraw:
                    draw_screen()
                else:
                    # Update only if position changed and both old and new positions are visible
                    if old_pos != current_pos:
                        # Check if old position is visible
                        if scroll_offset <= old_pos < scroll_offset + page_size:
                            # Update old position (remove arrow)
                            old_line_pos = header_lines + (old_pos - scroll_offset)
                            with term.location(0, old_line_pos):
                                print(term.clear_eol + draw_repo_line(old_pos, selected[old_pos], False))
                        
                        # Check if new position is visible
                        if scroll_offset <= current_pos < scroll_offset + page_size:
                            # Update new position (add arrow)
                            current_line_pos = header_lines + (current_pos - scroll_offset)
                            with term.location(0, current_line_pos):
                                print(term.clear_eol + draw_repo_line(current_pos, selected[current_pos], True))
                    elif key == ' ':  # Only selection changed, update current line
                        # Make sure current position is visible
                        if scroll_offset <= current_pos < scroll_offset + page_size:
                            current_line_pos = header_lines + (current_pos - scroll_offset)
                            with term.location(0, current_line_pos):
                                print(term.clear_eol + draw_repo_line(current_pos, selected[current_pos], True))
        
        # Return selected repositories
        return [repo for i, repo in enumerate(repos) if selected[i]]
            
    def bulk_delete(self, repos, dry_run=True, confirm=True, delay=1):
        """
        Delete multiple repositories
        
        Args:
            repos (list): List of repository objects to delete
            dry_run (bool): If True, only print which repos would be deleted
            confirm (bool): If True, ask for confirmation before deleting
            delay (float): Delay between deletions in seconds
        
        Returns:
            int: Number of repositories deleted
        """
        if not repos:
            print("No repositories to delete.")
            return 0
            
        # Use interactive selection if confirm is True
        if confirm:
            selected_repos = self.select_repositories_interactively(repos)
            
            if not selected_repos:
                print("No repositories selected for deletion.")
                return 0
            
            # Show selected repositories and confirm
            print("\nRepositories selected for deletion:")
            for i, repo in enumerate(selected_repos, 1):
                print(f"{i}. {repo['name']} ({repo['visibility']})")
            
            final_confirmation = input(f"\nAre you sure you want to delete these {len(selected_repos)} repositories? [y/N]: ")
            if final_confirmation.lower() != 'y':
                print("Operation cancelled.")
                return 0
        else:
            selected_repos = repos
            
        if dry_run:
            print("\nDRY RUN: No repositories were deleted.")
            return 0
                
        # Delete repositories
        deleted_count = 0
        for repo in selected_repos:
            if self.delete_repository(repo['name']):
                deleted_count += 1
                
            # Add delay to avoid rate limits
            if delay > 0 and repo != selected_repos[-1]:
                time.sleep(delay)
                
        print(f"\nOperation completed. Deleted {deleted_count} out of {len(selected_repos)} repositories.")
        return deleted_count

    def bulk_archive(self, repos, dry_run=True, confirm=True, delay=1):
        """
        Archive multiple repositories
        
        Args:
            repos (list): List of repository objects to archive
            dry_run (bool): If True, only print which repos would be archived
            confirm (bool): If True, ask for confirmation before archiving
            delay (float): Delay between operations in seconds
        
        Returns:
            int: Number of repositories archived
        """
        if not repos:
            print("No repositories to archive.")
            return 0
            
        # Use interactive selection if confirm is True
        if confirm:
            selected_repos = self.select_repositories_interactively(repos)
            
            if not selected_repos:
                print("No repositories selected for archiving.")
                return 0
            
            # Show selected repositories and confirm
            print("\nRepositories selected for archiving:")
            for i, repo in enumerate(selected_repos, 1):
                print(f"{i}. {repo['name']} ({repo['visibility']})")
            
            final_confirmation = input(f"\nAre you sure you want to archive these {len(selected_repos)} repositories? [y/N]: ")
            if final_confirmation.lower() != 'y':
                print("Operation cancelled.")
                return 0
        else:
            selected_repos = repos
            
        if dry_run:
            print("\nDRY RUN: No repositories were archived.")
            return 0
                
        # Archive repositories
        archived_count = 0
        for repo in selected_repos:
            if self.archive_repository(repo['name']):
                archived_count += 1
                
            # Add delay to avoid rate limits
            if delay > 0 and repo != selected_repos[-1]:
                time.sleep(delay)
                
        print(f"\nOperation completed. Archived {archived_count} out of {len(selected_repos)} repositories.")
        return archived_count

    def select_action_interactively(self):
        """
        Interactive UI to select action (archive/delete) using arrow keys
        
        Returns:
            str: Selected action ('archive' or 'delete') or None if cancelled
        """
        term = self.term
        actions = ['archive', 'delete']
        current_pos = 0
        
        def draw_screen():
            """Draw the action selection screen"""
            with term.location(0, 0):
                print(term.clear)
                print(term.bold + "Select action (use arrow keys, ENTER to confirm)" + term.normal)
                print("-" * term.width)
                
                for i, action in enumerate(actions):
                    if i == current_pos:
                        print(term.black_on_white(f"→ {action.capitalize()}"))
                    else:
                        print(f"  {action.capitalize()}")
                
                print("-" * term.width)
                print("↑/↓: Navigate | ENTER: Confirm | Q: Quit")
        
        # Initial draw
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            draw_screen()
            
            while True:
                key = term.inkey()
                
                if key.name == 'KEY_UP':
                    current_pos = max(0, current_pos - 1)
                    draw_screen()
                elif key.name == 'KEY_DOWN':
                    current_pos = min(len(actions) - 1, current_pos + 1)
                    draw_screen()
                elif key.name == 'KEY_ENTER':
                    return actions[current_pos]
                elif key == 'q':
                    return None
                    
        return None

    def process_repositories(self, repos, dry_run=True, confirm=True, delay=1):
        """
        Process repositories with interactive selection and action choice
        
        Args:
            repos (list): List of repository objects
            dry_run (bool): If True, only preview actions
            confirm (bool): If True, ask for confirmation
            delay (float): Delay between operations in seconds
        
        Returns:
            tuple: (action taken, number of repositories processed)
        """
        if not repos:
            print("No repositories found.")
            return None, 0
            
        # First, select repositories
        if confirm:
            selected_repos = self.select_repositories_interactively(repos)
            if not selected_repos:
                print("No repositories selected.")
                return None, 0
        else:
            selected_repos = repos
            
        # Then, select action
        action = self.select_action_interactively()
        if not action:
            print("Operation cancelled.")
            return None, 0
            
        # Show selection summary and confirm
        print(f"\nRepositories selected for {action}:")
        for i, repo in enumerate(selected_repos, 1):
            print(f"{i}. {repo['name']} ({repo['visibility']})")
            
        if confirm:
            final_confirmation = input(f"\nAre you sure you want to {action} these {len(selected_repos)} repositories? [y/N]: ")
            if final_confirmation.lower() != 'y':
                print("Operation cancelled.")
                return None, 0
                
        # Process based on selected action
        if action == 'delete':
            result = self.bulk_delete(selected_repos, dry_run=dry_run, confirm=False, delay=delay)
        else:  # archive
            result = self.bulk_archive(selected_repos, dry_run=dry_run, confirm=False, delay=delay)
            
        return action, result