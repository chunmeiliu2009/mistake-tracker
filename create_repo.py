import os
import requests
import subprocess

def setup_github_repository():
    try:
        # Verify GitHub token
        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            print("GitHub token is missing. Please provide a valid token.")
            return False

        # Test token validity
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        test_response = requests.get("https://api.github.com/user", headers=headers)
        if test_response.status_code != 200:
            print(f"Invalid GitHub token: {test_response.json().get('message', '')}")
            return False

        # GitHub API endpoint for creating a repository
        url = "https://api.github.com/user/repos"
        
        # Repository configuration
        data = {
            "name": "mistake-tracker",
            "description": "A web platform for students to track and learn from their homework mistakes",
            "private": False,
            "auto_init": False
        }

        # Create the repository
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 201:
            if response.status_code == 422:  # Repository already exists
                print("Repository already exists, proceeding with push...")
            else:
                print(f"Failed to create repository: {response.json().get('message', '')}")
                return False

        # Get the repository URL
        repo_url = f"https://github.com/{test_response.json()['login']}/mistake-tracker.git"
        
        # Configure git
        subprocess.run(['git', 'config', '--global', 'user.email', "replit@example.com"])
        subprocess.run(['git', 'config', '--global', 'user.name', "Replit User"])
        
        # Initialize git if not already initialized
        if not os.path.exists('.git'):
            subprocess.run(['git', 'init'])
        
        # Remove existing remote if it exists
        subprocess.run(['git', 'remote', 'remove', 'origin'], stderr=subprocess.DEVNULL)
        
        # Add new remote with token authentication
        repo_url_with_token = f"https://oauth2:{github_token}@github.com/{test_response.json()['login']}/mistake-tracker.git"
        subprocess.run(['git', 'remote', 'add', 'origin', repo_url_with_token])
        
        # Create .gitkeep in uploads directory
        os.makedirs('static/uploads', exist_ok=True)
        with open('static/uploads/.gitkeep', 'w') as f:
            pass
        
        # Add all files
        subprocess.run(['git', 'add', '.'])
        
        # Commit changes
        subprocess.run(['git', 'commit', '-m', 'Initial commit: Mistake Tracker web application'])
        
        # Force push to main branch
        result = subprocess.run(['git', 'push', '-f', '-u', 'origin', 'main'])
        
        if result.returncode == 0:
            print(f"Successfully pushed code to {repo_url}")
            return True
        else:
            print("Failed to push code to GitHub")
            return False
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    success = setup_github_repository()
    if success:
        print("Repository setup completed successfully!")
    else:
        print("Failed to setup repository.")
