import os
import requests
import subprocess

def setup_github_repository():
    # GitHub API endpoint for creating a repository
    url = "https://api.github.com/user/repos"
    
    # Repository configuration
    data = {
        "name": "mistake-tracker",
        "description": "A web platform for students to track and learn from their homework mistakes",
        "private": False
    }
    
    # Headers with authorization
    headers = {
        "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        # Create the repository
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 201:
            print(f"Failed to create repository: {response.json().get('message', '')}")
            return False

        # Get the repository URL from the response
        repo_url = response.json()['html_url']
        git_url = response.json()['clone_url']
        
        # Configure git
        subprocess.run(['git', 'config', '--global', 'user.email', "replit@example.com"])
        subprocess.run(['git', 'config', '--global', 'user.name', "Replit User"])
        
        # Remove existing remote if it exists
        subprocess.run(['git', 'remote', 'remove', 'origin'], stderr=subprocess.DEVNULL)
        
        # Add new remote
        token = os.environ['GITHUB_TOKEN']
        repo_url_with_token = git_url.replace('https://', f'https://oauth2:{token}@')
        subprocess.run(['git', 'remote', 'add', 'origin', repo_url_with_token])
        
        # Create .gitkeep in uploads directory
        os.makedirs('static/uploads', exist_ok=True)
        with open('static/uploads/.gitkeep', 'w') as f:
            pass
        
        # Add and commit all files
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'Initial commit: Mistake Tracker web application'])
        
        # Push to GitHub
        result = subprocess.run(['git', 'push', '-u', 'origin', 'main'])
        
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
