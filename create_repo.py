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
            "Authorization": f"token {github_token}",  # Changed to use 'token' instead of 'Bearer'
            "Accept": "application/vnd.github.v3+json"
        }
        test_response = requests.get("https://api.github.com/user", headers=headers)
        if test_response.status_code != 200:
            print(f"Invalid GitHub token: {test_response.json().get('message', '')}")
            return False

        # Get username from the test response
        username = test_response.json()['login']
        repo_name = "mistake-tracker"
        
        # Check if repository exists
        repo_check = requests.get(f"https://api.github.com/repos/{username}/{repo_name}", headers=headers)
        
        if repo_check.status_code != 200:
            # Create repository if it doesn't exist
            data = {
                "name": repo_name,
                "description": "A web platform for students to track and learn from their homework mistakes",
                "private": False,
                "auto_init": False
            }
            create_response = requests.post("https://api.github.com/user/repos", json=data, headers=headers)
            if create_response.status_code != 201:
                print(f"Failed to create repository: {create_response.json().get('message', '')}")
                return False

        # Configure git
        subprocess.run(['git', 'config', '--global', 'user.email', "replit@example.com"])
        subprocess.run(['git', 'config', '--global', 'user.name', "Replit User"])
        
        # Initialize git if not already initialized
        if not os.path.exists('.git'):
            subprocess.run(['git', 'init'])

        # Ensure uploads directory exists with .gitkeep
        os.makedirs('static/uploads', exist_ok=True)
        with open('static/uploads/.gitkeep', 'w') as f:
            pass

        # Set up remote
        remote_url = f"https://{github_token}@github.com/{username}/{repo_name}.git"
        
        # Remove existing remote if it exists
        subprocess.run(['git', 'remote', 'remove', 'origin'], stderr=subprocess.DEVNULL)
        subprocess.run(['git', 'remote', 'add', 'origin', remote_url])

        # Add and commit all files
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'Update: Fixed Feather icon and improved repository setup'])

        # Force push to main branch
        push_result = subprocess.run(['git', 'push', '-f', 'origin', 'main'])
        
        if push_result.returncode == 0:
            print(f"Successfully pushed code to https://github.com/{username}/{repo_name}")
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
        print("Repository setup and code push completed successfully!")
    else:
        print("Failed to setup repository or push code.")
