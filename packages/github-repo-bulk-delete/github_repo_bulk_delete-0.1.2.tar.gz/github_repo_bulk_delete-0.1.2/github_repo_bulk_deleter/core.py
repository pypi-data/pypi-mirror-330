"""
Core functionality for GitHub Repository Bulk Deleter
"""
import requests
import os
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
            params = {'per_page': 30, 'page': page}
            if visibility:
                params['type'] = visibility
                
            response = requests.get(
                f"{self.base_url}/user/repos", 
                headers=self.headers,
                params=params
            )
            
            if response.status_code != 200:
                print(f"Error fetching repositories: {response.status_code}")
                print(response.text)
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
            
    def select_repositories_interactively(self, repos):
        # ...existing code...
            
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