"""
GitHub Repository Bulk Deleter - A tool to interactively select and delete multiple GitHub repositories
"""
import requests
import os
import argparse
import time
from getpass import getpass
from blessed import Terminal

class GitHubRepoBulkDeleter:
    def __init__(self, token=None, username=None):
        self.token = token or os.environ.get('GITHUB_TOKEN') or getpass("Enter your GitHub personal access token: ")
        self.username = username or os.environ.get('GITHUB_USERNAME') or input("Enter your GitHub username: ")
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = 'https://api.github.com'
        self.term = Terminal()
        
    # ...existing code...
            
    def select_repositories_interactively(self, repos):
        """
        Interactive UI to select repositories using arrow keys and spacebar
        
        :param repos: List of repository objects
        :return: List of selected repositories
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
                print(term.bold + "Select repositories to delete (use arrow keys, SPACE to select, ENTER to confirm)" + term.normal)
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
        
        :param repos: List of repository objects to delete
        :param dry_run: If True, only print which repos would be deleted
        :param confirm: If True, ask for confirmation before deleting
        :param delay: Delay between deletions in seconds
        :return: Number of repositories deleted
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

def main():
    parser = argparse.ArgumentParser(description="Bulk delete GitHub repositories")
    parser.add_argument("--token", help="GitHub personal access token")
    parser.add_argument("--username", help="GitHub username")
    parser.add_argument("--pattern", help="Regex pattern to match repository names")
    parser.add_argument("--visibility", choices=["public", "private"], help="Filter by visibility")
    parser.add_argument("--no-confirm", action="store_true", help="Skip confirmation prompt")
    parser.add_argument("--dry-run", action="store_true", help="Only show which repos would be deleted")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between deletions in seconds")
    
    args = parser.parse_args()
    
    deleter = GitHubRepoBulkDeleter(token=args.token, username=args.username)
    repos = deleter.get_repositories(filter_pattern=args.pattern, visibility=args.visibility)
    deleter.bulk_delete(repos, dry_run=args.dry_run, confirm=not args.no_confirm, delay=args.delay)

# Entry point for the CLI
def cli_main():
    """Entry point for the CLI tool."""
    main()

if __name__ == "__main__":
    main()