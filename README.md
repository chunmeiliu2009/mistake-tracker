# Homework Mistake Tracker

## Project Overview
A web platform designed to help students track and learn from their homework mistakes. This application enables students to document their mistakes, understand where they went wrong, and improve their learning journey through systematic tracking and analysis.

## Features
- User Authentication (Email and Google OAuth)
- Problem Documentation
  - Title and subject categorization
  - Detailed description
  - Image upload support
- Dashboard View
  - Chronological display of problems
  - Subject-based organization
  - Visual representation with images
- Secure File Storage
  - Support for PNG, JPG, JPEG formats
  - 16MB file size limit

## Technologies Used
- Backend:
  - Python 3.11
  - Flask (Web Framework)
  - SQLAlchemy (ORM)
  - PostgreSQL (Database)
- Frontend:
  - Bootstrap 5 (Dark Theme)
  - Feather Icons
- Authentication:
  - Flask-Login
  - Google OAuth 2.0
- File Handling:
  - Werkzeug

## Installation & Setup
1. Clone the repository to your Replit workspace
2. Install required Python packages:
   ```bash
   pip install flask flask-sqlalchemy flask-login flask-wtf oauthlib requests Pillow
   ```
3. Set up environment variables (see Environment Variables section)
4. Initialize the database:
   ```python
   flask db upgrade
   ```
5. Start the development server:
   ```bash
   python app.py
   ```

## Environment Variables
The following environment variables are required:
- `FLASK_SECRET_KEY`: Secret key for Flask session management
- `DATABASE_URL`: PostgreSQL database connection URL
- `GOOGLE_OAUTH_CLIENT_ID`: Google OAuth client ID
- `GOOGLE_OAUTH_CLIENT_SECRET`: Google OAuth client secret

Database-specific variables (automatically set up on Replit):
- `PGUSER`: PostgreSQL username
- `PGPASSWORD`: PostgreSQL password
- `PGDATABASE`: Database name
- `PGHOST`: Database host
- `PGPORT`: Database port

## Usage Guide
1. Register an account using email or Google authentication
2. Log in to access your dashboard
3. Click "Add New Problem" to document a homework mistake:
   - Enter the problem title
   - Select the subject
   - Provide a detailed description
   - Upload an image (optional)
4. View all your documented problems on the dashboard
5. Track your progress and learning improvements over time

## Google OAuth Setup
1. Visit the [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new project or select an existing one
3. Go to the Credentials page
4. Click "Create Credentials" > "OAuth 2.0 Client ID"
5. Configure the OAuth consent screen
6. Add authorized redirect URI:
   ```
   https://YOUR_REPLIT_DOMAIN/google_login/callback
   ```
7. Copy the Client ID and Client Secret
8. Add them to your environment variables

## Contributing Guidelines
1. Fork the repository
2. Create a new branch for your feature
3. Follow the existing code style and organization
4. Write clear commit messages
5. Test your changes thoroughly
6. Submit a pull request with a detailed description

## Security Notes
- Never commit environment variables or sensitive information
- Always validate user input
- Use secure password hashing
- Implement proper file upload validation
- Keep dependencies updated
